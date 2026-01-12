from elevenlabs.conversational_ai.conversation import ClientTools
from langchain_community.tools import GoogleSearchRun

from dotenv import load_dotenv

import os
from google import genai
from google.genai import types
import requests
import base64
from PIL import Image
from io import BytesIO


load_dotenv()

def searchWeb(parameters):
    query = parameters.get("query")
    result = GoogleSearchRun.run(query = query)
    return result

def save_to_txt(parameters):
    filename = parameters.get("filename")
    data = parameters.get("data")

    formatted_data = f"{data}"

    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_data + "\n")

def create_html_file(parameters):
    filename = parameters.get("filename")
    data = parameters.get("data")
    title = parameters.get("title")

    formatted_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <div>{data}</div>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as file:
        file.write(formatted_html)



def generate_image(parameters):
    prompt = parameters.get("prompt")
    filename = parameters.get("filename")
    size = parameters.get("size", "1024x1024")
    save_dir = parameters.get("save_dir", "generated_images")

    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_images(
        model="imagen-3.0-generate-001",
        prompt=prompt,
        image_size=size,
    )

    image_base64 = response.images[0].image_base64
    image_bytes = base64.b64decode(image_base64)

    image = Image.open(BytesIO(image_bytes))
    image.save(filepath)




client_tools = ClientTools()

client_tools.register("searchWeb", searchWeb)
client_tools.register("saveToTxt", save_to_txt)
client_tools.register("createHtmlFile", create_html_file)
client_tools.register("generateImage", generate_image)

