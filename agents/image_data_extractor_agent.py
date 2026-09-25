
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
            
        except Exception:
            logger.exception("Unexpected error in init")
            raise
    