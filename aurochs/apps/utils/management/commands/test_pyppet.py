import asyncio
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

from twisted.internet import reactor
import scrapy
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerProcess
from django.conf import settings as django_settings

settings = {k: v for k, v in django_settings.__dict__.items() if not k.startswith("_")}

# from myproject.Ox import OxSpider
from pyppeteer import launch


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        asyncio.get_event_loop().run_until_complete(self.handle_pyppeteer())

    async def handle_pyppeteer(self, *args, **kwargs):
        browser = await launch()
        page = await browser.newPage()

        start_urls = [
            "https://example.com",
            "https://www.airbnb.com/rooms/676486381352575052",
            "https://www.linkedin.com/in/christophervharper",
        ]
        for p in start_urls:
            await page.goto(p)
            content = await page.content()
            print(p)
            print(content)

        await browser.close()
