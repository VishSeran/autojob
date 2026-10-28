from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from ai_backend.llm_handler.vision_llm import VisionLLmHandler
from configs.logger import get_logger
from schema.job_image_schema import JobDetails

logger = get_logger("image-data-extractor-agent")

class ImageDataExtractorAgent:
    
    
    def __init__(self):
        
        try:
            
            vision_llm_handler = VisionLLmHandler()
            self.vision_llm = vision_llm_handler.get_vision_llm().with_structured_output(
                JobDetails
            )
            
            # self.prompt = ChatPromptTemplate.from_messages(
            #     [
            #         (
            #             "system",
            #              """
            #             You are a job advertisement image extraction agent.

            #             The provided images contain information from a job vacancy
            #             advertisement.

            #             Extract only information that is visibly available in the
            #             provided images.

            #             Extract:
            #             - description: Job description or overview
            #             - responsibilities: Duties and responsibilities
            #             - requirements: Qualifications, skills, experience, education,
            #             and other candidate requirements

            #             Do not invent, infer, or fabricate information that is not
            #             visible in the images.

            #             If a particular category is not available, return null.
            #         """
            #         ),
            #         (
            #             "human",
            #             "{images}"
            #         )
            #     ]
            # )
            
            self.system_prompt = """
                You are a job advertisement image extraction agent.

                Analyze all provided job advertisement images.

                Extract only information visibly present in the images.

                Extract:
                - job_title
                - company_email
                - company_contact
                - description
                - responsibilities
                - requirements
                - salary

                Do not invent or infer missing information.

                If a field is unavailable, return null.
                """
            
            logger.info("Image data ectractor agent is created")
            
        except Exception:
            logger.exception("Unexpected error in init")
            raise
        
        
    async def get_vision_response(self, images):
        
        try:
            
            if not images:
                logger.warning("Job urls are empty")
                
            message = [
                SystemMessage(
                    content=self.system_prompt
                ),
                HumanMessage(
                    content= [
                        {
                            "type": "text",
                            "text": (
                                "Extract the job advertisement "
                                "details from these images."
                            )
                        },
                        *images
                    ]
                )
            ]
            
            response = await self.vision_llm.ainvoke(
                message
            )
            logger.info(f"Vision response is fetched: \n{response}")
            
            return response
        
        except ValueError:
            logger.exception("Unexpected value error in get vision respponse")
            raise
            
        except Exception:
            logger.exception("Unexpected error in get vision respponse")
            raise
    