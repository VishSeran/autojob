import asyncio

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from ai_backend.llm_handler.vision_llm import VisionLLmHandler
from schema.job_image_schema import JobDetails

image_urls = [
    "https://www.topjobs.lk//logo/DEFZZZ/7297c1144.jpg",
   
]

image_content = [
    {
        "type": "image_url",
        "image_url": {
            "url": url
        }
    }
    for url in image_urls
]

async def main():
    handler = VisionLLmHandler()
    llm = handler.get_vision_llm().with_structured_output(
        JobDetails,
        # strict=True,
        # method="json_schema"
    )

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": (
                    "Describe exactly what you can see "
                    "in this image. Transcribe all readable "
                    "text. Do not invent information."
                ),
            },
            *image_content
        ]
    )

    response = await llm.ainvoke([message])

    print(response)

asyncio.run(main())