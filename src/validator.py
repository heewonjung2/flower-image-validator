import os
import json
import base64

from dotenv import load_dotenv
from openai import OpenAI

from prompt import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def encode_image(uploaded_image) -> str:
    """업로드 이미지를 Base64 문자열로 변환"""

    image_bytes = uploaded_image.read()

    return base64.b64encode(image_bytes).decode("utf-8")


def call_openai(prompt: str, base64_image: str) -> str:
    """OpenAI Vision API 호출"""

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
            }
        ]
    )

    return response.output_text


def validate_flower(prompt: str, uploaded_image) -> dict:
    """꽃 이미지 검증"""

    base64_image = encode_image(uploaded_image)

    result = call_openai(
        prompt,
        base64_image
    )

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        raise ValueError(
            f"GPT가 JSON이 아닌 응답을 반환했습니다.\n\n{result}"
        )