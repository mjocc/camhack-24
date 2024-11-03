from openai import OpenAI
from transformers import pipeline
from mistralai import Mistral
import time
import os

classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True,
)
model = "mistral-small-latest"
mistral_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=mistral_key)


def classify_image(image_b64: bytes):
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
                            "url": f"data:image/jpeg;base64,{image_b64.decode("utf-8")}",
                        },
                    },
                ],
            }
        ],
    )

    return completion


def generate_response(person, text, tokens):
    messages = [
        {"role": "system", "content": person},
        {"role": "user", "content": text},
    ]
    chat_response = client.chat.complete(
        model=model, max_tokens=tokens, messages=messages
    )
    time.sleep(2)
    return chat_response.choices[0].message.content


def run_scenario(p1name, p2name, p1type, p2type, p1occ, p2occ, situation):
    p1 = f"Your name is {p1name}. You are {p1type}. Currently you are a(n) {p1occ}, and found yourself in the following situation: {situation}. "
    p2 = f"Your name is {p2name}. You are {p2type}. Currently you are a(n) {p2occ}, and found yourself in the following situation: {situation}. "
    p1r = generate_response(p1, " Start the conversation with: Hello!", 100)
    p2r = generate_response(p2, f" Respond to: {p1r}", 100)
    context = (
        f"Considering the context: Start of sentence: {p1r} Start of sentence: {p2r}"
    )

    p1_list = [p1r]
    p2_list = [p2r]

    for i in range(1, 3):
        p1_list.append(generate_response(p1, context + p2_list[i - 1], 100))
        context += f"They just said: {p1_list[i]} "
        p2_list.append(generate_response(p2, context + p1_list[i], 100))
        context += f"They just said: {p2_list[i]} "

    weighted_sum1 = []
    weighted_sum2 = []
    weights = {
        "anger": -1,
        "disgust": -1,
        "fear": -1,
        "joy": 1,
        "neutral": 0,
        "sadness": -1,
        "surprise": 1,
    }

    for p in p1_list:
        classification = classifier(p)[0]
        weighted_sum1.append(
            sum(item["score"] * weights[item["label"]] for item in classification)
        )

    for p in p2_list:
        classification = classifier(p)[0]
        weighted_sum2.append(
            sum(item["score"] * weights[item["label"]] for item in classification)
        )

    avg1 = sum(weighted_sum1) / len(weighted_sum1) if weighted_sum1 else 0
    avg2 = sum(weighted_sum2) / len(weighted_sum2) if weighted_sum2 else 0

    avg = (avg1 + avg2) / 2
    percentage = (avg + 1) / 0.02
    return percentage


def generate_dialogue(p1name, p2name, p1type, p2type, p1occ, p2occ, situation):
    p1 = f"Your name is {p1name}. You are {p1type}. Currently you are a(n) {p1occ}, and found yourself in the following situation: {situation}. "
    p2 = f"Your name is {p2name}. You are {p2type}. Currently you are a(n) {p2occ}, and found yourself in the following situation: {situation}. "
    return generate_response(
        "You are a writer",
        f"Generate a dialogue between {p1} and {p2} in {situation}",
        400,
    )
