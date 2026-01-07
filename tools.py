from elevenlabs.conversational_ai.conversation import ClientTools
from langchain_community.tools import GoogleSearchRun

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

client_tools = ClientTools()

client_tools.register("searchWeb", searchWeb)
client_tools.register("saveToTxt", save_to_txt)


