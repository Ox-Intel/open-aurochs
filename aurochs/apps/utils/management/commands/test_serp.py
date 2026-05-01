# flake8: noqa: E501
import datetime
import ast
import re
import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from bs4 import BeautifulSoup
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
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
    def handle_chris(self, *args, **kwargs):
        llm = OpenAI(temperature=0.2)
        # tools = load_tools(["serpapi", "llm-math", "requests", "wikipedia"], llm=llm)
        tools = load_tools(["serpapi", "python_repl"], llm=llm)
        agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )
        topic = "Chris V Harper from Torch Capital"
        # name = "Analytical Thinking"
        name = "Leadership"
        question = "evaluate how well a potential hire is for an investment associate role at our company"
        context = ""

        # [{'name': 'Mathematical proficiency', 'weight': 10, 'description': 'Strong mathematical proficiency is necessary to be successful in this role.'}, {'name': 'Analytical skills', 'weight': 10, 'description': 'Excellent analytical skills are necessary to be successful in this role.'}, {'name': 'Communication skills', 'weight': 10, 'description': 'Excellent communication skills are necessary to be successful in this role.'}, {'name': 'Attention to detail', 'weight': 10, 'description': 'Keen attention to detail is necessary to be successful in this role.'}, {'name': 'Finance degree', 'weight': 8, 'description': 'A bachelor's degree in finance is preferred for this role.'}, {'name': 'Portfolio management experience', 'weight': 8, 'description': 'Several years of private equity or corporate portfolio management experience is preferred for this role.'

        # scoring_response = agent.run(f"Using both the internet and your general knowledge, evaluate how strongly {topic} scores for {name}, in helping the user {question}. {context}.  If you run into trouble searching or requesting a link, please ignore it and continue. In using wikipedia, make absolutely sure that the subject matches before including it.  Please return a single number between 1 and 10, where where 1 is very weakly supported and 10 is very strongly supported, followed by a |, followed by a brief explanation of why that score was given. Cite all URLs or sources used to make the assessment. Do not include anything besides the number score before the | character.  For example, \n8 | This is an explanation." )
        scoring_response = agent.run(
            f"Please use all of: serp and the internet, wikipedia (only if an exact match is found) and your general knowledge.   If you run into trouble searching or requesting a link, please ignore it and continue. In using wikipedia, make absolutely sure that the subject matches before including it.  Evaluate how strongly {topic} scores for {name}, in helping the user {question}. {context}.  Please return a single number between 1 and 10, where where 1 is very weakly supported and 10 is very strongly supported, followed by a |, followed by a brief explanation of why that score was given. Cite any URLs used to make the assessment. Do not include anything besides the number score before the | character.  For example, \n8 | This is an explanation."
        )
        print(scoring_response)

    def handle(self, *args, **kwargs):
        llm = OpenAI(temperature=0.2)
        # tools = load_tools(["serpapi", "llm-math", "requests", "wikipedia"], llm=llm)
        tools = load_tools(["serpapi", "llm-math", "python_repl"], llm=llm)
        agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )
        topic = "France"
        topic = "Costa Rica"
        # name = "Analytical Thinking"
        # name = "Transportation safety"
        # context = " Understanding the safety and reliability of transportation options, such as public transportation or rental cars, is important in preventing accidents or other risks."
        name = "Terrorism threat"
        context = " The threat of terrorism is a key factor in assessing travel risks. Countries with a high risk of terrorism may have increased security measures and restrictions on travel."
        question = "understand foreign country travel risks"

        chat_llm = ChatOpenAI(temperature=0.5)
        prompt = PromptTemplate(
            input_variables=["question", "name"],
            template="In the context of {question}, is {name} a positive, good sentiment or a bad, negative sentiment?  Return 1 for positive and -1 for negative. Please only return the number.",
        )

        chain = LLMChain(llm=chat_llm, prompt=prompt)
        chat_response = chain.run({"question": question, "name": name})
        print(chat_response)
        weak_score = 1
        strong_score = 10

        # [{'name': 'Mathematical proficiency', 'weight': 10, 'description': 'Strong mathematical proficiency is necessary to be successful in this role.'}, {'name': 'Analytical skills', 'weight': 10, 'description': 'Excellent analytical skills are necessary to be successful in this role.'}, {'name': 'Communication skills', 'weight': 10, 'description': 'Excellent communication skills are necessary to be successful in this role.'}, {'name': 'Attention to detail', 'weight': 10, 'description': 'Keen attention to detail is necessary to be successful in this role.'}, {'name': 'Finance degree', 'weight': 8, 'description': 'A bachelor's degree in finance is preferred for this role.'}, {'name': 'Portfolio management experience', 'weight': 8, 'description': 'Several years of private equity or corporate portfolio management experience is preferred for this role.'

        # scoring_response = agent.run(f"Using both the internet and your general knowledge, evaluate how strongly {topic} scores for {name}, in helping the user {question}. {context}.  If you run into trouble searching or requesting a link, please ignore it and continue. In using wikipedia, make absolutely sure that the subject matches before including it.  Please return a single number between 1 and 10, where where 1 is very weakly supported and 10 is very strongly supported, followed by a |, followed by a brief explanation of why that score was given. Cite all URLs or sources used to make the assessment. Do not include anything besides the number score before the | character.  For example, \n8 | This is an explanation." )
        # Include every URL visited when generating the score and explanation.
        scoring_response = agent.run(
            f"Please use all of: serpapi and the internet, wikipedia (only if an exact match is found) and your general knowledge.   If you run into trouble searching or requesting a link, please ignore it and continue. In using wikipedia, make absolutely sure that the subject matches before including it.  Evaluate how strongly {topic} scores for {name}, in helping the user {question}. {context}.  Please return a single number between 1 and 10, where where {weak_score} is very weakly supported and {strong_score} is very strongly supported, followed by a |, followed by a brief explanation of why that score was given. Cite all URLs or sources used to make the assessment. Cite all URLs or sources used to make the assessment. Test to make sure that included citations are real links.  Do not include anything besides the number score before the | character.  For example, \n8 | This is an explanation."
        )
        print(scoring_response)
        if chat_response == "-1":
            print("invert")
