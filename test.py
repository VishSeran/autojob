import asyncio
import logging

from ai_backend.agents.image_data_extractor_agent import ImageDataExtractorAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def main():

    print("=" * 70)
    print("Testing ImageDataExtractorAgent")
    print("=" * 70)

    # Use one real TopJobs image URL
    image_url = (
        "https://www.topjobs.lk//logo/0000000375/1034cghana.png"
    )

    images = [
        {
            "type": "image_url",
            "image_url": {
                "url": image_url
            }
        }
    ]

    print("\n[1] Creating ImageDataExtractorAgent...")

    try:
        agent = ImageDataExtractorAgent()
        print("✓ Agent created successfully")

    except Exception as e:
        print("✗ Failed to create agent")
        print(f"Error: {e}")
        return

    print("\n[2] Testing image URL validation...")

    try:
        is_valid = await agent.validate_image_url(
            image_url
        )

        print(f"Image URL valid: {is_valid}")

        if not is_valid:
            print("✗ Image validation failed")
            return

        print("✓ Image URL validation successful")

    except Exception as e:
        print("✗ Image validation raised an exception")
        print(f"Error: {e}")
        return

    print("\n[3] Testing Base64 + Groq Vision request...")
    print("This may take a few seconds...\n")

    try:
        response = await agent.get_vision_response(
            images
        )

        print("=" * 70)
        print("VISION RESPONSE")
        print("=" * 70)

        print(response)

        print("\n" + "=" * 70)
        print("✓ TEST PASSED")
        print("=" * 70)

    except Exception as e:
        print("=" * 70)
        print("✗ TEST FAILED")
        print("=" * 70)

        print(f"\nError type: {type(e).__name__}")
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())