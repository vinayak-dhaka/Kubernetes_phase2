import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def extract_json(content: str) -> dict:
    json_text = content[content.find("{"):content.rfind("}") + 1]
    return json.loads(json_text)

def get_model():
    return ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
        temperature=0.0,
    )
