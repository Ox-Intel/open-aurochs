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

from twisted.internet import reactor
import scrapy
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerProcess
from django.conf import settings as django_settings

settings = {k: v for k, v in django_settings.__dict__.items() if not k.startswith("_")}

# from myproject.Ox import OxSpider


class OxSpider(scrapy.Spider):
    name = "oxspider"
    start_urls = [
        "https://www.airbnb.com/rooms/676486381352575052",
        "https://www.linkedin.com/in/christophervharper",
    ]
    start_urls = [
        "https://www.linkedin.com/in/christophervharper",
    ]
    start_urls = [
        "https://www.nbcnews.com/media/fox-news-sends-tucker-carlson-cease-desist-letter-new-twitter-show-rcna88842",
    ]

    custom_settings = {
        "HTTPERROR_ALLOWED_CODES": [999],
    }

    def start_requests(self):
        for url in self.start_urls:
            url = f"{url}?_escaped_fragment_="
            yield SplashRequest(
                url,
                self.parse,
                meta={"dont_redirect": False},
                args={
                    "wait": 2,
                    "http_headers": {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                    },
                    "private_mode": True,
                    "media_source": "media",
                },
            )

    def parse(self, response):
        # scrape something
        # print(response.__dict__)
        print(response.text)
        text_nodes = response.xpath(
            "//*[not(self::script or self::style)]/text()"
        ).getall()

        title = response.css("title::text").get()
        url = response.url
        text = " ".join(text_nodes)
        print("\n\n")
        print(title)
        print("\n")
        print(url)
        print("\n")
        print(text)
        yield


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        runner = CrawlerProcess(settings)
        d = runner.crawl(OxSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()  # the script will block here until the crawling is finished
