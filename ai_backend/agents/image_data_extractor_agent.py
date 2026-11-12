import base64

import httpx
from langchain_core.messages import HumanMessage, SystemMessage

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

                Analyze all provided job advertisement images and extract ONLY information
                that is visibly present in the images.

                Extract the following fields:

                - job_title
                - company_email
                - company_contact
                - description
                - responsibilities
                - requirements
                - salary

                IMPORTANT DEFINITION OF company_email:

                "company_email" does NOT mean any general company email address.

                For this task, "company_email" specifically means the email address that
                the employer instructs candidates to use for submitting their CV/resume
                or applying for the advertised job.

                For example, if the advertisement says:

                    "Send your CV to careers@abc.com"

                then:
                    company_email = "careers@abc.com"

                If it says:

                    "Interested candidates should email their CV to hr@abc.com"

                then:
                    company_email = "hr@abc.com"

                If it says:

                    "Please send your resume to jobs@abc.com"

                then:
                    company_email = "jobs@abc.com"

                DO NOT use a general company email address such as:
                - info@company.com
                - contact@company.com
                - support@company.com

                unless the advertisement explicitly instructs candidates to send their
                CV/resume or job application to that address.

                If multiple email addresses are visible, select the email address that is
                specifically associated with submitting the CV/resume or job application.

                If an email address is present but its purpose is unclear, do not assume
                that it is the application email. Return null.

                Do not invent, infer, or construct an email address.

                Extract only information visibly present in the advertisement images.

                If a field is unavailable, return null.
                """
            
            logger.info("Image data ectractor agent is created")
            
        except Exception:
            logger.exception("Unexpected error in init")
            raise
        
        
    async def validate_image_url(self, img_url:str) -> bool:
        
        try:
            
            async with httpx.AsyncClient(
                timeout=10.0,
                follow_redirects=True
            ) as client:
                
                response = await client.get(
                    img_url,
                    headers= {
                        "User-Agent": "Mozilla/5.0"
                    }
                ) 
            
                if response.status_code != 200:
                    logger.Warning(
                        f"Invalid image URL: {img_url} "
                        f"(status={response.status_code})"     
                    )
                    return False
                
                
                content_type = response.headers.get(
                    "content-type", ""
                )
                
                
                
                if not content_type.startswith("image/"):
                    logger.warning(
                        f"URL does not return an image: {img_url} "
                        f"(content-type={content_type})"
                    )
                    return False
                
            return True
        
        except httpx.RequestError as e:
            logger.warning(
                f"Failed to download image: {img_url} - {e}"
            )
            return False
            
        except Exception:
            logger.exception("Unexpected error in validate image url")
            return False
        
        
    async def get_vision_response(self, images):
        
        try:
            
            if not images:
                logger.warning("Job urls are empty")
                
            validate_images = []
            
            for image in images:
                
                if not isinstance(image, dict):
                    logger.warning(
                        f"Invalid image object: {image}"
                    )
                    continue
                
                img_url = image['image_url']['url']
                
                if not img_url:
                    logger.warning(
                        "Image object does not contain image_url"
                    )
                    continue
                
                is_valid = await self.validate_image_url(img_url)
                
                if not is_valid:
                    logger.warning(
                        f"Skipping invalid image: {img_url}"
                    )
                    continue
                
                async with httpx.AsyncClient(
                    timeout=10.0,
                    follow_redirects=True
                ) as client:
                    
                    data = await client.get(
                        img_url,
                        headers= {
                            "User-Agent": "Mozilla/5.0"
                        }
                    )
                    
                    content = data.content
                    content_type = data.headers.get(
                        "content-type",
                        ""
                    ).lower()
                    
                    encoded_img = base64.b64encode(
                        content
                    ).decode("utf-8")
                
                    
                validate_images.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{content_type};base64,{encoded_img}"
                    }
                })
                
            message = [
                SystemMessage(
                    content=self.system_prompt
                ),
                HumanMessage(
                     content=[
                        {
                            "type": "text",
                            "text": (
                                "Analyze the provided job advertisement image(s). "
                                "Read all visible text carefully and extract the "
                                "job information according to the system instructions."
                            ),
                        },
                        *validate_images
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
    