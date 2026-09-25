from langchain_core.prompts import ChatPromptTemplate

from configs.logger import get_logger
from llm_handler.vision_llm import VisionLLmHandler
from schema.job_image_schema import JobImageDetails

logger = get_logger("image-data-extractor-agent")

class ImageDataExtractorAgent:
    
    
    def __init__(self):
        
        try:
            
            vision_llm_handler = VisionLLmHandler
            self.vision_llm = vision_llm_handler.get_vision_llm().with_structured_output(
                JobImageDetails
            )
            
            self.prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                         """
                        You are a job advertisement image extraction agent.

                        The provided images contain information from a job vacancy
                        advertisement.

                        Extract only information that is visibly available in the
                        provided images.

                        Extract:
                        - description: Job description or overview
                        - responsibilities: Duties and responsibilities
                        - requirements: Qualifications, skills, experience, education,
                        and other candidate requirements

                        Do not invent, infer, or fabricate information that is not
                        visible in the images.

                        If a particular category is not available, return null.
                    """
                    ),
                    (
                        "human",
                        "{images}"
                    )
                ]
            )
            
            self.chain = self.prompt | self.vision_llm
            logger.info("Image data ectractor agent is created")
            
        except Exception:
            logger.exception("Unexpected error in init")
            raise
        
        
    async def get_vision_response(self, images):
        
        try:
            
            response = await self.chain.ainvoke({
                "images": images
            })
            logger.info("Vision response is fetched")
            
            return response
        
        except ValueError:
            logger.exception("Unexpected value error in get vision respponse")
            raise
            
        except Exception:
            logger.exception("Unexpected error in get vision respponse")
            raise
    