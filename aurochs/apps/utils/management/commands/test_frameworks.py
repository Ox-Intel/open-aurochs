# flake8: noqa: E501
import datetime
import ast
import re
import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from bs4 import BeautifulSoup
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from api.events.base import BaseEventHandler
from reports.models import Report
from collaboration.models import ObjectSubscription
from frameworks.models import Framework
from sources.models import Source
from stacks.models import Stack
from organizations.models import GenericPermission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        llm = OpenAI(temperature=0.2)
        # tools = load_tools(["serpapi", "llm-math", "requests", "wikipedia"], llm=llm)
        tools = load_tools(
            [
                "serpapi",
                "llm-math",
            ],
            llm=llm,
        )
        agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )
        topic = "Wells Fargo"
        name = "Analytical Thinking"
        question = "pick a bank for my small business"
        framework_context = ""

        # scoring_response = agent.run(f"Using both the internet and your general knowledge, evaluate how strongly {topic} scores for {name}, in helping the user {question}. {context}.  If you run into trouble searching or requesting a link, please ignore it and continue. In using wikipedia, make absolutely sure that the subject matches before including it.  Please return a single number between 1 and 10, where where 1 is very weakly supported and 10 is very strongly supported, followed by a |, followed by a brief explanation of why that score was given. Cite all URLs or sources used to make the assessment. Do not include anything besides the number score before the | character.  For example, \n8 | This is an explanation." )
        # scoring_response = agent.run(f"Please make a list of the 4-8 most important criteria for {question}. {framework_context}. Do not number the list, or put parenthesis around any scores. Please also add to each criteria a number between 1 and 10 indicating how important this criteria is, where 1 is not important and 10 is very important. Please include a short explanation of each criteria.  Please return the criteria as a python list, with each item being a dictionary with keys for the name, weight, and description. The keys should be lowercase, and the dictionary should be valid python." )
        # scoring_response = llm.run(f"Please make a list of the 4-8 most important criteria for {question}. {framework_context}. Do not number the list, or put parenthesis around any scores. Please also add to each criteria a number between 1 and 10 indicating how important this criteria is, where 1 is not important and 10 is very important. Please include a short explanation of each criteria.  Please return the criteria as a python list, with each item being a dictionary with keys for the name, weight, and description. The keys should be lowercase, and the dictionary should be valid python." )

        llm = ChatOpenAI(temperature=0.5)
        prompt = PromptTemplate(
            input_variables=["question", "framework_context"],
            template="Please make a bulleted list of the 4-8 most important criteria for {question}. {framework_context}. Do not number the list, or put parenthesis around any scores. Please also add to each criteria a number between 1 and 10 indicating how important this criteria is, where 1 is not important and 10 is very important. Please include a short explanation of each criteria. Please separate the criteria name and score with a colon and the score and description with |.  For example: \n Criteria Name: 5 | Criteria explanation is here. ",
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        chat_response = chain.run(
            {"question": question, "framework_context": framework_context}
        )
        print(chat_response)

        # for r in ast.literal_eval(chat_response):
        #     print(f"{r['weight']} - {r['name']}: {r['description']}")

        roles = []

        llm = OpenAI(temperature=0.9)
        prompt = PromptTemplate(
            input_variables=[
                "question",
            ],
            template="Can you make me a list of four jobs that are best qualified at {question}? Please only return the job titles, and separate them by commas. Do not number the list or include any numbers.",
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        role_response = chain.run(
            {
                "question": question,
            }
        )
        print(role_response)
        raw_roles = role_response.split(",")
        for r in raw_roles:
            if r.strip():
                roles.append(r.strip())
        print(roles)
        role_frameworks = {}

        for role in roles:
            llm = ChatOpenAI(temperature=0.5)
            prompt = PromptTemplate(
                input_variables=["question", "framework_context", "role"],
                template="You are an expert {role}, tasked with communicating a decision-making framework rooted in your professional experience.  Please make a bulleted list of the 4-8 most important criteria for {question}. {framework_context}. Do not number the list, or put parenthesis around any scores. Please also add to each criteria a number between 1 and 10 indicating how important this criteria is, where 1 is not important and 10 is very important. Please include a short explanation of each criteria. Please separate the criteria name and score with a colon and the score and description with |.  For example: \n Criteria Name: 5 | Criteria explanation is here. ",
            )

            chain = LLMChain(llm=llm, prompt=prompt)
            chat_response = chain.run(
                {
                    "question": question,
                    "framework_context": framework_context,
                    "role": role,
                }
            )
            print("\n\n")
            print(role)
            print(chat_response)
            role_frameworks[role] = chat_response

        role_framework_text = ""
        for role, fw_text in role_frameworks.items():
            role_framework_text += f"{fw_text}\n\n"

        llm = OpenAI(temperature=0.2)
        prompt = PromptTemplate(
            input_variables=[
                "question",
                "framework_context",
                "role_framework_text",
            ],
            template="""Below are four expert decision-making frameworks for {question}. Please combine them into one framework, producing a bulleted list of the 4-8 most important criteria for {question}. {framework_context}. Do not number the list, or put parenthesis around any scores. Please also add to each criteria a number between 1 and 10 indicating how important this criteria is, where 1 is not important and 10 is very important. Please include a short explanation of each criteria.  Ensure that every criteria has a complete sentence in its explanation. Please separate the criteria name and score with a colon and the score and description with |.  For example: 

Criteria Name: 5 | Criteria explanation is here.
{role_framework_text}
""",
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        combined_response = chain.run(
            {
                "question": question,
                "role_framework_text": role_framework_text,
                "framework_context": framework_context,
            }
        )

        print("\n\ncombined_response")
        print(combined_response)
