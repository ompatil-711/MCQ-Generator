from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_community.callbacks import get_openai_callback
import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
import PyPDF2

load_dotenv()
key = os.getenv("OPENAI_KEY")

llm = ChatOpenAI(openai_api_key=key, model="gpt-3.5-turbo", temperature=0.7)

# with open("..\..\Response.json","r") as f:
#     RESPONSE_JSON = json.load(f)


TEMPLATE = """
Text: {text}
You are an expert MCQ maker. Given the above text. It is your job to \
create a quize of {number} multiple choice question for subject in {tone} tone.
Make sure the question are not repeated and check all the question confirming the text as well.
Make sure to format the reposne like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{RESPONSE_JSON}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "RESPONSE_JSON"],
    template=TEMPLATE
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt,output_key="quiz", verbose=True)

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE2)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain = SequentialChain(chains=[quiz_chain,review_chain], input_variables=["text","number","subject","tone","RESPONSE_JSON"], output_variables=["quiz","review"], verbose=True)