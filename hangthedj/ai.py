from openai import OpenAI


def classify_image(image_b64):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Create a personality trait profile from this Instagram profile to be used as parameters in a compatibility app. Be truthful, don't worry about hurting their feelings. These 10 parameters should be single words or phrases. Structure your response as follows: parameter 1, parameter 2, parameter 3. There should be no additional text.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}",
                        },
                    },
                ],
            }
        ],
    )
