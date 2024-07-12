from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import base64
import requests

load_dotenv(find_dotenv())

def mermaid_code_generator(user_input):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)

    template = """
    You are a helpful designer assistant that returns Mermaid Markdown syntax/code that can be copy pasted and used to render customizable diagrams, charts and visualizations.
    Your goal is to help the user quickly create Mermaid code they can copy paste to visualize their ideas. You are to ONLY output mermaid code that will be copy pasted into a mermaid visualizer.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "Here's the idea to convert into mermaid code. Make sure to only output mermaid code and no other text: {user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input)

    return response

def generate_mermaid_image(mermaid_code):
    url = "https://mermaid.ink/img/"
    encoded_code = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("utf-8")
    image_url = f"{url}{encoded_code}"
    
    # Test if the URL is accessible
    response = requests.get(image_url)
    if response.status_code == 200:
        return image_url
    else:
        raise ValueError(f"Failed to access image URL: {image_url}")
