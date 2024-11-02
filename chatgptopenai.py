import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

secret_key = os.getenv("OPENAI_API_KEY")


client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Create a personality trait profile from this photo to be used as parameters in a compatability app. Be mean. These 10 parameters should be single words or phrases. Structure these parameters as follows: parameter 1, parameter 2, parameter 3. ",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://i.ibb.co/ZxSxTKj/IMG-7239.png",
                    },
                },
            ],
        }
    ],
)
