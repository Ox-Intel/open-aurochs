import datetime
import ast
import json
import re
import requests
import subprocess
from django.contrib.auth import authenticate, login
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
from api.tasks import (
    return_oxgpt,
    oxgpt_generate_framework,
    oxgpt_analyze_subjects,
    oxgpt_generate_subjects,
    oxgpt_generate_more_criteria,
    oxgpt_analyze_file,
)
from collaboration.models import ObjectSubscription
from frameworks.models import Framework, Criteria
from reports.models import Report, Scorecard, ScorecardScore
from organizations.models import Organization, Team, User
from stacks.models import Stack
from organizations.models import GenericPermission
from django.contrib.contenttypes.models import ContentType


class GenerateMoreCriteriaHandler(BaseEventHandler):
    direct_event = True

    def handle_event(self, request, data):
        # print(data)
        oxgpt_generate_more_criteria.delay(data, self.user_channel_id)
        data = {}

        return {
            "direct_event": True,
            "data": data,
            "success": True,
        }


class GenerateFrameworkHandler(BaseEventHandler):
    direct_event = True

    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        # print(data)

        oxgpt_generate_framework.delay(data, self.user_channel_id)
        data = {}

        return {
            "direct_event": True,
            "data": data,
            "success": True,
        }


class AnalyzeSubjectsHandler(BaseEventHandler):
    direct_event = True

    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        # print(data)
        oxgpt_analyze_subjects.delay(data, self.user_channel_id)
        data = {}

        return {
            "direct_event": True,
            "data": data,
            "success": True,
        }


class AnalyzeFileHandler(BaseEventHandler):
    direct_event = True

    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        # print(data)
        oxgpt_analyze_file.delay(data, self.user_channel_id)
        data = {"content": ""}

        return {
            "direct_event": True,
            "data": data,
            "success": True,
        }


class GenerateSubjectsHandler(BaseEventHandler):
    direct_event = True

    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        # print(data)
        oxgpt_generate_subjects.delay(data, self.user_channel_id)
        data = {}

        return {
            "direct_event": True,
            "data": data,
            "success": True,
        }


class CreateAccountHandler(BaseEventHandler):
    direct_event = True

    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        error_message = "Error creating account."
        try:
            if (
                "email" not in data
                or "password" not in data
                or "first_name" not in data
                or "last_name" not in data
            ):
                error_message = "All fields are required."
            else:
                if User.objects.filter(email=data["email"]).count() > 0:
                    error_message = (
                        "Email already in use.  Please try logging in instead."
                    )
                else:
                    user = User.objects.create(
                        username=data["email"], email=data["email"]
                    )
                    user.set_password(data["password"])
                    user.first_name = data["first_name"]
                    user.last_name = data["last_name"]
                    user.public_signup = True
                    user.save()
                    user = authenticate(
                        username=data["email"], password=data["password"]
                    )
                    if user is not None:
                        login(request, user)

                    return {
                        "direct_event": True,
                        "data": {
                            "success": True,
                            "ox_id": user.ox_id,
                        },
                        "success": True,
                    }

        except:
            pass

        data = {"success": False, "error_message": error_message}
        return {
            "direct_event": True,
            "data": data,
            "success": True,
        }


class LogInHandler(BaseEventHandler):
    direct_event = True

    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        error_message = "Username and password combination are not valid."
        try:
            if "email" not in data or "password" not in data:
                error_message = "All fields are required."
            else:
                for u in User.objects.filter(email__iexact=data["email"]).all():
                    if u.check_password(data["password"]):
                        login(request, u)
                        error_message = ""
                        return {
                            "direct_event": True,
                            "data": {
                                "success": True,
                                "ox_id": u.ox_id,
                            },
                            "success": True,
                        }
        except:
            import traceback

            traceback.print_exc()

        data = {"success": False, "error_message": error_message}
        return {
            "direct_event": True,
            "data": data,
            "success": True,
        }


class SaveResultsHandler(BaseEventHandler):
    # direct_event = True

    def handle_event(self, request, data):
        # Return all objects created or modified, and success true or false.
        # print(data)
        topic = data.get("topic")
        if not topic:
            topic = "Blank"
        topic_context = data.get("topic_context")
        subjects = data.get("subjects")
        scoring_context = data.get("scoring_context")
        framework = data.get("framework")
        scorecards = data.get("scorecards")
        public_oxid = data.get("public_oxid")
        password = data.get("password")
        urlsUsed = data.get("urlsUsed")
        docNames = data.get("docNames")
        report_id = data.get("report_id", None)
        user = request.user
        first_public_user_save = False
        if request.user.ox_id == public_oxid:
            first_public_user_save = True
        if request.user.is_anonymous and public_oxid and password:
            u = User.objects.get(ox_id=public_oxid)
            user = authenticate(u.username, password)
            if user is not None:
                login(request, user)
                request.user = user
                first_public_user_save = True
            else:
                raise Exception("Unknown user")

        subject_list = subjects.split("\n")
        ret_list = []

        if "description" in framework:
            description = framework["description"]
        else:
            description = framework["subtitle"]
        if "id" in framework:
            f = Framework.authorized_objects.authorize(user=user).get(
                ox_id=framework["id"]
            )
            framework_criteria = {}
            for c in f.criteria:
                framework_criteria[c.name] = c
        else:
            f = Framework.authorized_objects.authorize(user=user).create(
                name=framework["name"],
                subtitle=description,
                gpt_prompt=topic,
                gpt_context=topic_context,
            )
            f.created_by = user
            f.modified_by = user
            f.save()

            framework_criteria = {}
            for crit in framework["criteria"]:
                # print(crit)
                c = Criteria.objects.create(framework=f, **crit)
                framework_criteria[crit["name"]] = c
        ret_list.append(f)

        reports_dict = {}
        r = None
        for sc_data in scorecards:
            # print(sc_data)
            subject = sc_data["name"]
            if report_id:
                r = Report.authorized_objects.authorize(user=user).get(ox_id=report_id)
            else:
                r = Report.authorized_objects.authorize(user=user).create(
                    name=subject,
                    gpt_prompt=subject,
                    gpt_context=scoring_context,
                )
                r.created_by = user
                r.modified_by = user
            if urlsUsed or len(docNames) > 0:
                if r.notes:
                    notes = r.notes[: r.notes.rfind("]}")] + ", "
                    notes = notes.replace(",,", ",")
                else:
                    notes = "{ops:["
            if urlsUsed:
                notes += "{insert:'Urls Referenced:\\n'},"
                for url in urlsUsed:
                    notes += (
                        "{attributes:{link:"
                        + f"'{url}'"
                        + "},insert:"
                        + f"'{url}\\n'"
                        + "},"
                    )

            if len(docNames) > 0:
                notes += "{insert:'\\nDocs Referenced:\\n'},"
                for d in docNames:
                    notes += "{insert:" + f"'{d}\\n'" + "},"

            if urlsUsed or len(docNames) > 0:
                notes += "]}"
                # print(notes)
                r.notes = notes
            r.save()
            reports_dict[subject] = r

            sc = Scorecard.objects.create(
                report=r,
                framework=f,
                scorer=user,
                created_by=user,
                modified_by=user,
            )
            sc.save()
            # Add scores
            for sc_score in sc_data["scores"]:
                c = framework_criteria[sc_score["criteria"]["name"]]
                scs, _ = ScorecardScore.objects.get_or_create(
                    scorecard=sc,
                    criteria=c,
                )
                scs.score = sc_score["score"]
                scs.gpt_score = sc_score["gpt_score"]
                scs.gpt_scored_last = sc_score["gpt_scored_last"]
                scs.skipped = sc_score["skipped"]
                scs.comment = sc_score["comment"]
                scs.created_by = user
                scs.modified_by = user
                scs.save()

            ret_list.append(r)
            ret_list.append(sc)

        if len(subject_list) > 1:
            # Make a stack
            s = Stack.authorized_objects.authorize(user=user).create(
                name=topic,
            )
            s.created_by = user
            s.modified_by = user
            if urlsUsed or len(docNames) > 0:
                notes = "{ops:["
                if s.notes:
                    notes = s.notes[: s.notes.rfind("]}")]
                    notes = notes.replace(",,", ",")
                else:
                    notes = "{ops:["

            if urlsUsed:
                notes += "{insert:'Urls Referenced:\\n'},"
                for url in urlsUsed:
                    notes += (
                        "{attributes:{link:"
                        + f"'{url}'"
                        + "},insert:"
                        + f"'{url}\\n'"
                        + "},"
                    )

            if len(docNames) > 0:
                notes += "{insert:'\\nDocs Referenced:\\n'},"
                for d in docNames:
                    notes += "{insert:" + f"'{d}\\n'" + "},"

            if urlsUsed or len(docNames) > 0:
                notes += "]}"
                s.notes = notes

            for name, r in reports_dict.items():
                s.reports.add(r)
            s.save()
            ret_list.append(s)
            target_obj = s
        else:
            target_obj = r

        if first_public_user_save:
            self.direct_event = True
            return {
                "direct_event": True,
                "data": {
                    "target_obj_type": f"{target_obj.__class__.__name__.lower()}",
                    "target_obj_id": f"{target_obj.pk}",
                    "target_obj_ox_id": f"{target_obj.ox_id}",
                },
                "success": True,
            }

        return {
            "obj_list": ret_list,
            "success": True,
            "target_obj": target_obj,
        }
