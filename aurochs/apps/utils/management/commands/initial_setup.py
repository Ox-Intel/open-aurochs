# flake8: noqa
import json
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.core.management import call_command
from decimal import Decimal


def boolean_input(question, default=None):
    result = input("%s " % question)
    if not result and default is not None:
        return default
    while len(result) < 1 or result[0].lower() not in "yn":
        result = input("Please answer y (yes) or n (no): ")
    return result[0].lower() == "y"


def add_gps(obj, organization):
    from django.contrib.contenttypes.models import ContentType
    from organizations.models import GenericPermission

    ct = ContentType.objects.get_for_model(obj)
    gp, _ = GenericPermission.objects.get_or_create(
        content_type=ct, object_id=obj.pk, organization=organization
    )
    gp.can_score = True
    gp.can_read = True
    gp.can_write = True
    gp.can_administer = True
    gp.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from archives.models import HistoricalEvent
        from frameworks.models import Criteria, Framework
        from organizations.models import (
            Organization,
            Team,
            TeamMember,
            User,
            OrganizationRole,
            GenericPermission,
        )
        from reports.models import Report, Scorecard, ScorecardScore
        from sources.models import Source, SourceFeedback
        from django.contrib.contenttypes.models import ContentType

        print("============================")
        print("   ✓ Ox Intel System Setup")
        print("============================")
        print("")

        print("Ensuring superuser...")
        superuser_exists = User.objects.filter(is_superuser=True).count() > 0
        if not superuser_exists:
            if not boolean_input(
                "No superuser found.  Would you like to create one? (y/n) "
            ):
                print(
                    "Skipping superuser creation.  Please re-run setup in the future to create one."
                )
            else:
                call_command("createsuperuser")
                print("  ✓ Superuser created.")
        else:
            print("  ✓ Superuser found.")
        su = User.objects.filter(is_superuser=True).all().first()
        print("")

        org_exists = Organization.objects.all().count() > 0
        o = Organization.objects.all().first()
        create_org = False
        if org_exists:
            if not boolean_input(
                f"Organization {o.name} found.  Would you like to use it for installation? (y/n)"
            ):
                create_org = True
        else:
            if not boolean_input(
                "No organizations found.  Would you like to create one? (y/n)"
            ):
                print(
                    "Skipping organization creation, and all example content installation.  To install example content, please re-run setup."
                )
            else:
                create_org = True
        if create_org:
            confirmed = False
            while not confirmed:
                org_name = input(
                    "What is the name of the organization you would like to create? "
                )
                if Organization.objects.filter(name=org_name).count() > 0:
                    if boolean_input(
                        f"Organization named '{org_name}' exists.  Use it? (y/n)"
                    ):
                        confirmed = True
                else:
                    if boolean_input(
                        f"Create an organization called '{org_name}'? (y/n)"
                    ):
                        confirmed = True
            o, _ = Organization.objects.get_or_create(name=org_name)
            print(f"  ✓ Organization {o.name} created.")
            o.add_user(su, can_manage=True)
            o.save()
            print(f"  ✓ Added superuser to {o.name} Organization.")

        print("")
        print("Ensuring example user...")
        if User.objects.filter(username="example").all().count() == 0:
            xu, _ = User.objects.get_or_create(username="example")
            xu.first_name = "Example"
            xu.last_name = "User"
            xu.email = "none@example.com"
            xu.save()
            print("  ✓ Created Example User.")
        else:
            xu = User.objects.filter(username="example").all().first()
            print("  ✓ Found Example User.")
        o.add_user(xu)
        o.save()
        print(f"  ✓ Added to {o.name} Organization.")
        print("")

        if not boolean_input(
            f"Would you like to install the example frameworks and reports into {o.name} Organization? (y/n)"
        ):
            print(
                "  x Skipping all example content installation.  To install example content, please re-run setup."
            )
        else:
            if (
                Framework.objects.filter(
                    name="Example: Iraq WMD Source Framework"
                ).count()
                > 0
                or Framework.objects.filter(
                    name="Example: HUMINT Source Reliability"
                ).count()
                > 0
                or Framework.objects.filter(
                    name="Example: ICD 203: Analytic Standards"
                ).count()
                > 0
                or Framework.objects.filter(name="Example: Rigor").count() > 0
                or Report.objects.filter(name="Example: Iraq WMD").count() > 0
                or Report.objects.filter(
                    name="Example: Curveball: Iraq Mobile WMDs"
                ).count()
                > 0
                or Report.objects.filter(
                    name="Example: UNSCOM Inspector: Iraq Disarmament"
                ).count()
                > 0
                or Report.objects.filter(
                    name="Example: Kamal: Iraq Disarmament"
                ).count()
                > 0
                or Source.objects.filter(name="Hussein Kamal").count() > 0
                or Source.objects.filter(name="Curveball").count() > 0
                or Source.objects.filter(name="UNSCOM Inspector").count() > 0
            ):
                if boolean_input(
                    "Found existing example content. Would you like to clear it, for a fresh install? (Recommended) (y/n)"
                ):
                    Framework.raw_objects.filter(
                        name="Example: Iraq WMD Source Framework"
                    ).all().delete()
                    Framework.raw_objects.filter(
                        name="Example: HUMINT Source Reliability"
                    ).all().delete()
                    Framework.raw_objects.filter(
                        name="Example: ICD 203: Analytic Standards"
                    ).all().delete()
                    Framework.raw_objects.filter(name="Example: Rigor").all().delete()
                    Report.raw_objects.filter(name="Example: Iraq WMD").all().delete()
                    Report.raw_objects.filter(
                        name="Example: Curveball: Iraq Mobile WMDs"
                    ).all().delete()
                    Report.raw_objects.filter(
                        name="Example: UNSCOM Inspector: Iraq Disarmament"
                    ).all().delete()
                    Report.raw_objects.filter(
                        name="Example: Kamal: Iraq Disarmament"
                    ).all().delete()
                    Source.raw_objects.filter(name="Hussein Kamal").all().delete()
                    Source.raw_objects.filter(name="Curveball").all().delete()
                    Source.raw_objects.filter(name="UNSCOM Inspector").all().delete()
                    for gp in GenericPermission.objects.all():
                        if gp.content_object is None:
                            gp.delete()
                    print("  ✓ Cleared existing example content.")

            print("Adding example frameworks and reports...")

            f_icd, created = Framework.objects_with_deleted.get_or_create(
                name="Example: ICD 203: Analytic Standards",
                description="This Intelligence Community Directive (ICD) establishes the Intelligence Community (IC) Analytic Standards that govern the production and evaluation of analytic products; articulates the responsibility of intelligence analysts to strive for excellence, integrity, and rigor in their analytic thinking and work practices; and delineates the role of the Office of Director of National Intelligence (ODNI) Analytic Ombuds. \n\nThe IC Analytic Standards guide analysis and analytic production. All IC analytic products shall be consistent with the five Analytic Standards encompassed in this Framework. \n\nSource: https://www.dni.gov/files/documents/ICD/ICD%20203%20Analytic%20Standards.pdf",  # noqa
            )
            f_icd.created_by = xu
            f_icd.created_by = xu
            f_icd.save()

            c, _ = Criteria.objects.get_or_create(
                name="Independent of political consideration",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = "Analytic assessments must not be distorted by, nor shaped for, advocacy of a particular audience, agenda, or policy viewpoint. Analytic judgments must not be influenced by the force of preference for a particular policy."  # noqa
            c.weight = Decimal("5.0")
            c.index = 0
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Timely",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = "Analysis must be disseminated in time for it to be actionable by customers. Analytic elements have the responsibility to be continually aware of events of intelligence interest, of customer activities and schedules, and of intelligence requirements and priorities, in order to provide useful analysis at the right time."  # noqa
            c.weight = Decimal("5.0")
            c.index = 1
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Objective",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = "Analysts must perform their functions with objectivity and with awareness of their own assumptions and reasoning. They must employ reasoning techniques and practical mechanisms that reveal and mitigate bias. Analysts should be alert to influence by existing analytic positions or judgments and must consider alternative perspectives and contrary information. Analysis should not be unduly constrained by previous judgments when new developments indicate a modification is necessary."  # noqa
            c.weight = Decimal("5.0")
            c.index = 2
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Based on all available sources of information",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = "Analysis should be informed by all relevant information available. Analytic elements should identify and address critical information gaps and work with collection activities and data providers to develop access and collection strategies."  # noqa
            c.weight = Decimal("5.0")
            c.index = 3
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Quality and Credibility",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = "Properly describes quality and credibility of underlying sources, data, and methodologies."  # noqa
            c.weight = Decimal("5.0")
            c.index = 4
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Explains Uncertainties",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = "Properly expresses and explains uncertainties associated with major analytic judgments."  # noqa
            c.weight = Decimal("5.0")
            c.index = 5
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Distinguishes Assumptions and Judgments",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = "Properly distinguishes between underlying intelligence information and analysts' assumptions and judgments."  # noqa
            c.weight = Decimal("5.0")
            c.index = 6
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Analysis of Alternatives",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = "Incorporates analysis of alternatives."  # noqa
            c.weight = Decimal("5.0")
            c.index = 7
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Customer Relevance",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = (
                "Demonstrates customer relevance and addresses implications."  # noqa
            )
            c.weight = Decimal("5.0")
            c.index = 8
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Clear and Logical",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = "Uses clear and logical argumentation."  # noqa
            c.weight = Decimal("5.0")
            c.index = 9
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Explains Change and Consistency",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = (
                "Explains change to or consistency of analytic judgments."  # noqa
            )
            c.weight = Decimal("5.0")
            c.index = 10
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Accuracy",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = "Makes accurate judgments and assessments."  # noqa
            c.weight = Decimal("5.0")
            c.index = 11
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Visually Effective",
                framework=f_icd,
            )
            c.created_by = xu
            c.description = (
                "Incorporates effective visual information where appropriate."  # noqa
            )
            c.weight = Decimal("5.0")
            c.index = 12
            c.save()

            add_gps(f_icd, o)
            print("  ✓ Example Framework: ICD 203")

            f_rigor, created = Framework.objects_with_deleted.get_or_create(
                name="Example: Rigor",
                description="A framework for measuring rigor developed by Daniel J. Zelik, Emily S. Patterson, and David D. Woods. The framework measures whether sufficient considerations were made or precautions taken in the process of making sense of an issue. The Ox score from this framework communicates the level of rigor of the crafted intelligence product. \n\nSource: https://www.researchgate.net/publication/228809190_Understanding_rigor_in_information_analysis",  # noqa
            )
            f_rigor.created_by = xu
            f_rigor.modified_by = xu
            f_rigor.save()

            c, _ = Criteria.objects.get_or_create(
                name="Hypothesis Explanation",
                framework=f_rigor,
            )
            c.created_by = xu
            c.description = "Hypothesis Exploration describes the extent to which multiple hypotheses were considered in explaining data. In a low rigor process there is minimal weighing of alternatives. A high-rigor process, in contrast, involves broadening of the hypothesis set beyond an initial framing and incorporating multiple perspectives to identify the best, most probably explanations."  # noqa
            c.weight = Decimal("10.0")
            c.index = 0
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Sensitivity Analysis",
                framework=f_rigor,
            )
            c.created_by = xu
            c.description = "Sensitivity Analysis considers the extent to which the analyst considers and understands the assumptions and limitations of their analysis. In a low-rigor process, explanations seem appropriate and valid on a surface level. In a high-rigor process the analyst employs a strategy to consider the strength of explanations if individual supporting sources were to prove invalid."  # noqa
            c.weight = Decimal("10.0")
            c.index = 1
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Information Validation",
                framework=f_rigor,
            )
            c.created_by = xu
            c.description = "Information Validation details the levels at which information sources are corroborated and cross-validated. In a low-rigor process little effort is made to use converging evidence to verify source accuracy, while a high-rigor process includes a systematic approach for verifying information and, when possible, ensures the use of sources closest to the area of interest."  # noqa
            c.weight = Decimal("10.0")
            c.index = 2
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Explanation Critique",
                framework=f_rigor,
            )
            c.created_by = xu
            c.description = "Explanation Critique is a different form of collaboration that captures how many different perspectives were incorporated in examining the primary hypotheses. In a low-rigor process, there is little use of other analysts to give input on explanation quality. In a high-rigor process peers and experts have examined the chain of reasoning and explicitly identified which inferences are stronger and which are weaker."  # noqa
            c.weight = Decimal("10.0")
            c.index = 3
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Information Synthesis",
                framework=f_rigor,
            )
            c.created_by = xu
            c.description = "Information Synthesis refers to how far beyond simply collecting and listing data an analyst went in their process. In the low-rigor process an analyst simply compiles the relevant information in a unified form, whereas a high-rigor process has extracted and integrated information with a thorough consideration of diverse interpretations of relevant data."  # noqa
            c.weight = Decimal("10.0")
            c.index = 4
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Specialist Collaboration",
                framework=f_rigor,
            )
            c.created_by = xu
            c.description = "Specialist Collaboration describes the degree to which an analyst incorporates the perspectives of domain experts into their assessments. In a low-rigor process little effort is made to seek out such expertise, while in a high-rigor process the analyst has talked to, or may be, a leading expert in the key content areas of the analysis."  # noqa
            c.weight = Decimal("10.0")
            c.index = 5
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Information Search",
                framework=f_rigor,
            )
            c.created_by = xu
            c.description = "Information Search relates to the depth and breadth of the search process used in collecting data. A low rigor analysis process does not go beyond routine and readily available data sources, whereas a high rigor process attempts to exhaustively explore all data potentially available in the relevant sample space."  # noqa
            c.weight = Decimal("10.0")
            c.index = 6
            c.save()

            c, _ = Criteria.objects.get_or_create(
                name="Stance Analysis",
                framework=f_rigor,
            )
            c.created_by = xu
            c.description = "Stance Analysis is the evaluation of data with the goal of identifying the stance or perspective of the source and placing it into a broader context of understanding. At the low-rigor level an analyst may notice a clear bias in a source, while a high-rigor process involves research into source backgrounds with the intent of gaining a more subtle understanding of how their perspective might influence their stance toward analysis-relevant issues."  # noqa
            c.weight = Decimal("10.0")
            c.index = 7
            c.save()

            add_gps(f_rigor, o)
            print("  ✓ Example Framework: Rigor")

            f_iraq, _ = Framework.objects.get_or_create(
                name="Example: Iraq WMD Source Framework"
            )
            f_iraq.description = "Framework built by former Executive Director of the CIA for evaluating Iraq's efforts to build a WMD capability."
            f_iraq.save()

            c1, _ = Criteria.objects.get_or_create(
                name="MASINT and trace elements", framework=f_iraq
            )
            c1.description = "Detection of signatures associated with WMD programs would indicate past activity and possible ongoing activity"
            c1.weight = Decimal("9.0")
            c1.index = 0
            c1.save()

            c2, _ = Criteria.objects.get_or_create(
                name="HUMINT including UNSCOM inspectors", framework=f_iraq
            )
            c2.description = "Clandestine collection and on-site inspections can provide confirmation of on-going programs as well as evidence that Iraq has destroyed its stockpiles of chemical and biological agents and ended efforts to acquire fissile material"
            c2.weight = Decimal("9.0")
            c2.index = 1
            c2.save()

            c3, _ = Criteria.objects.get_or_create(name="SIGINT", framework=f_iraq)
            c3.description = "Intercepted communications between government entities engaged in WMD programs historically or military units would reveal the current state of WMD programs as long as the communications are “first-hand” and unambiguous"
            c3.weight = Decimal("9.0")
            c3.index = 2
            c3.save()

            c4, _ = Criteria.objects.get_or_create(
                name="History and lack of cooperation with inspectors", framework=f_iraq
            )
            c4.description = "Incomplete or inaccurate disclosures of WMD materials and facilities and an effort to obstruct inspectors is consistent with efforts to hide a WMD program, but such efforts can also be explained by Hanlon’s Razor"
            c4.weight = Decimal("6.0")
            c4.index = 3
            c4.save()

            c5, _ = Criteria.objects.get_or_create(name="Overhead", framework=f_iraq)
            c5.description = "Overhead can reveal activity and security precautions around possible WMD facilities, but it cannot reveal what is happening inside a building or lab"
            c5.weight = Decimal("6.0")
            c5.index = 4
            c5.save()

            c6, _ = Criteria.objects.get_or_create(
                name="Unknown unknowns", framework=f_iraq
            )
            c6.description = (
                "Indicators of Iraqi behavior not covered by the other variables"
            )
            c6.weight = Decimal("3.0")
            c6.index = 5
            c6.save()

            c7, _ = Criteria.objects.get_or_create(
                name="Facilities and equipment capable of supporting a WMD program",
                framework=f_iraq,
            )
            c7.description = (
                "Equipment that is dual use is quite common in WMD programs"
            )
            c7.weight = Decimal("5.0")
            c7.index = 6
            c7.save()
            add_gps(f_iraq, o)
            print("  ✓ Example Framework: Iraq WMD Source")

            f_humint, _ = Framework.objects.get_or_create(
                name="Example: HUMINT Source Reliability"
            )
            f_humint.description = "Framework created by former Deputy Executive Director of the CIA Marty Petersen for evaluating HUMINT sources."
            f_humint.save()

            c8, _ = Criteria.objects.get_or_create(
                name="Source access to information", framework=f_humint
            )
            c8.description = "Source has access to the information in the claim"
            c8.weight = Decimal("10.0")
            c8.index = 0
            c8.save()

            c9, _ = Criteria.objects.get_or_create(
                name="Source motivation", framework=f_humint
            )
            c9.description = "The source's motivation in making the claim is clear"
            c9.weight = Decimal("10.0")
            c9.index = 1
            c9.save()

            c10, _ = Criteria.objects.get_or_create(
                name="Source consistency", framework=f_humint
            )
            c10.description = (
                "The source's story is consistent with no significant holes"
            )
            c10.weight = Decimal("7.0")
            c10.index = 2
            c10.save()

            c11, _ = Criteria.objects.get_or_create(
                name="Information reasonability", framework=f_humint
            )
            c11.description = "The information in the claim is reasonable"
            c11.weight = Decimal("8.0")
            c11.index = 3
            c11.save()

            c12, _ = Criteria.objects.get_or_create(
                name="Direct contact", framework=f_humint
            )
            c12.description = "We have direct contact with the source. 10 for direct, face-to-face interaction, which gives the collecting entity a change to vet and observe over time the behavior and motivation of the source"
            c12.weight = Decimal("5.0")
            c12.index = 4
            c12.save()

            c13, _ = Criteria.objects.get_or_create(
                name="Unknown unknowns", framework=f_humint
            )
            c13.description = "This variable represents the unexpected or unforeseeable conditions and considerations that cannot be anticipated or accounted for based on past experience. NOTE: the score for this variable is inverse to the others. A 10 means we have a solid grip on the Unknowns, a zero the opposite."
            c13.weight = Decimal("5.0")
            c13.index = 5
            c13.save()

            c14, _ = Criteria.objects.get_or_create(
                name="Outside verification", framework=f_humint
            )
            c14.description = (
                "We have other means to verify the information in the claim"
            )
            c14.weight = Decimal("5.0")
            c14.index = 6
            c14.save()
            add_gps(f_humint, o)
            print("  ✓ Example Framework: HUMINT Source Reliability")

            # Public sources:
            # https://nsarchive2.gwu.edu/NSAEBB/NSAEBB234/WMD_report_excerpt.pdf
            # https://www.nytimes.com/1995/08/12/world/the-in-iraqi-who-counted-himself-out.html
            if Source.objects.filter(name="Hussein Kamal").count() > 0:
                s_hussein = Source.objects.filter(name="Hussein Kamal").all().first()
            else:
                s_hussein, _ = Source.objects.get_or_create(name="Hussein Kamal")
                s_hussein.description = "Hussein Kamal was the son-in-law and second cousin of Iraqi leader Saddam Hussein."
                s_hussein.save()
            add_gps(s_hussein, o)
            print("  ✓ Example Source: Hussein Kamal")

            # Public sources:
            # https://nsarchive2.gwu.edu/NSAEBB/NSAEBB234/index.htm
            # https://nsarchive2.gwu.edu/NSAEBB/NSAEBB234/SSCI_phaseI_excerpt.pdf
            # https://nsarchive2.gwu.edu/NSAEBB/NSAEBB234/WMD_report_excerpt.pdf
            # https://www.nytimes.com/2011/02/16/world/middleeast/16curveball.html
            # https://www.theguardian.com/world/2011/feb/15/defector-admits-wmd-lies-iraq-war
            if Source.objects.filter(name="Curveball").count() > 0:
                s_curveball = Source.objects.filter(name="Curveball").all().first()
            else:
                s_curveball, _ = Source.objects.get_or_create(name="Curveball")
                s_curveball.description = "Curveball is a human source managed by an allied intelligence service"
                s_curveball.save()
            add_gps(s_curveball, o)
            print("  ✓ Example Source: Curveball")

            # Public sources:
            # https://www.armscontrol.org/act/2000-06/features/case-iraqs-qualitative-disarmament
            # https://www.washingtonpost.com/wp-srv/inatl/longterm/iraq/stories/unscom101198.htm
            # https://nsarchive2.gwu.edu/NSAEBB/NSAEBB234/Leitenberg32006.html
            if Source.objects.filter(name="UNSCOM Inspector").count() > 0:
                s_unscom = Source.objects.filter(name="UNSCOM Inspector").all().first()
            else:
                s_unscom, _ = Source.objects.get_or_create(name="UNSCOM Inspector")
                s_unscom.description = (
                    "Inspector Ritter with United Nations Special Commission (UNSCOM)"
                )
                s_unscom.save()
            add_gps(s_unscom, o)
            print("  ✓ Example Source: UNSCOM")

            # Public sources:
            # https://nsarchive2.gwu.edu/NSAEBB/NSAEBB234/WMD_report_excerpt.pdf
            # https://www.nytimes.com/2004/01/26/world/struggle-for-iraq-intelligence-ex-inspector-says-cia-missed-disarray-iraqi-arms.html
            # https://nation.time.com/2012/09/06/iraq-how-the-cia-says-it-blew-it-on-saddams-wmd/
            r_iraq, _ = Report.objects.get_or_create(name="Example: Iraq WMD")
            r_iraq.summary = "Date: October 2002 Although Western intelligence agencies knew before the First Gulf War that Saddam was pursuing WMD on a large scale and had demonstrated a willingness to use chemical weapons against Iran and the Kurds in northern Iraq, intelligence communities were surprised by the scope and sophistication of Saddam’s WMD programs, especially his nuclear program. As a condition for ending the First Gulf War, Saddam was required to declare his WMD stocks and destroy them. In 2002 there was still much skepticism in the US and British intelligence communities that Saddam had declared everything and that he had indeed destroyed everything. This doubt was a critical concern as the US led coalition prepared for Operation Iraqi Freedom, the major justification for which was the belief that Saddam had retained a WMD capability and was probably increasing WMD stockpiles. \n\nASSUMPTIONS: \n- Saddam has the intent to develop, deploy, and use weapons of mass destruction. - Saddam sees WMD as a factor that restrains Iranian and Western military action against Iraq and increases his prestige and power in the Arab world. \n\nSources of information under HUMINT: Curveball, UNSCOM inspectors, and Hussein Kamal. What the variables indicate is that some combination of the UNSCOM findings and clandestine collection will give us the best insight into the current state of Saddam’s efforts to develop a WMD capability. Overhead and equipment are less valuable than might first be thought because BW and CW programs in particular are easy to hide and elaborate security around facilities is the norm in Iraq. Dual-use equipment is a possible indicator, but because it is dual-use it has legitimate uses other than supporting a WMD program. Lack of cooperation with inspectors and a history of inaccurate or misleading declarations is suspicious, but it may also be a reflection of Iraqi inefficiency and resentment of UNSCOM. \n\nFindings: The case for Iraq WMD rests mostly on history with some supporting SIGINT and limited HUMINT, which in itself is not compelling one way or the other. Facilities and dual use equipment are intriguing, but without more inspections or better HUMINT their true purposes cannot be established. The absence of MASINT is particularly concerning, as is the repeated use of caveats in the NIE, which point to the limited extent of our actual knowledge. Greater clarity on this issue probably rests on obtaining better HUMINT and best of all, if it can be achieved, the reintroduction of inspectors. Analysts would also be well advised to consider additional reasons for Iraq’s behavior besides hiding a WMD program. The variables do not include political or strategic factors that undoubtedly play some role in what is happening in Iraq. The second assumption needs a deeper examination. \n\nConclusion: The final OX Score on Iraq WMD--48%--indicates that Saddam having WMD is a 50-50 proposition and that more information is needed.\n\nAnalytic Question: What constitutes evidence of a WMD program and a WMD capability and how strong is that evidence in the case of Iraq?"
            r_iraq.save()
            r_iraq.frameworks.add(f_iraq)
            r_iraq.sources.add(s_hussein)
            r_iraq.sources.add(s_curveball)
            r_iraq.sources.add(s_unscom)
            r_iraq.save()

            sc, _ = Scorecard.objects.get_or_create(
                report=r_iraq, framework=f_iraq, scorer=xu
            )

            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c1)
            scs.score = Decimal("1.0")
            scs.comment = "Forensic evidence revealed degraded products from VX on metal fragments, but this was from 1998."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c2)
            scs.score = Decimal("5.0")
            scs.comment = "The HUMINT evidence is intriguing but not compelling one way or the other. Additional HUMINT collection or verification by the other variables is needed. Until that is available, the HUMINT must be treated with caution."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c3)
            scs.score = Decimal("7.0")
            scs.comment = "In his UN presentation, Powell plays intercepted conversations that reference modified mobile vehicles and nerve agents but primarily focus non-cooperation with inspectors."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c4)
            scs.score = Decimal("8.0")
            scs.comment = "The best interpretation that can be put on Iraq’s declarations is that they are incomplete, reluctant, and late. There is also a clear pattern of obstruction of UN inspectors and efforts at denial and deception. Iraq’s initial declarations on BW activity were patently false, and Baghdad has been unable to adequately account for all the BW growth material it declared. The rating allows for the possibility that Hanlon’s Razor can explain some of this."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c5)
            scs.score = Decimal("6.0")
            scs.comment = "Photography reveals considerable activity deemed unusual and suspicious at suspected WMD sites, including chemical storage bunkers. The NIE, however, states that accurate information is hard to obtain."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c6)
            scs.score = Decimal("0.0")
            scs.comment = "The NIE is replete with phrases like: “unable to collaborate”; “hard to estimate”; “cannot rule out”; “our information is limited”; and many “coulds.”"
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c7)
            scs.score = Decimal("5.0")
            scs.comment = "Iraq either possesses or has tried to procure equipment suitable for the manufacturing of WMD and built (and in some cases rebuilt) facilities that have potential WMD connections. The Intelligence Community is sharply divided on the aluminum tubes and magnet issues."
            scs.save()
            add_gps(r_iraq, o)
            print("  ✓ Example Report: Iraq WMD")

            r_curveball, _ = Report.objects.get_or_create(
                name="Example: Curveball: Iraq Mobile WMDs"
            )
            r_curveball.summary = "An Iraqi chemical engineer in Germany claims that Iraq has a mobile BW production capability and that is one reason why nothing definitive has turned up on overhead. The source is under the control of the BND.\n\nAnalytic Question: Are Curveball claim's regarding Iraq's production of mobile WMDs credible?"
            r_curveball.frameworks.add(f_humint)
            r_curveball.sources.add(s_curveball)
            r_curveball.feedback_score = 0
            r_curveball.feedback_comment = "Curveball admitted to lying."
            r_curveball.save()

            sc, _ = Scorecard.objects.get_or_create(
                report=r_curveball, framework=f_humint, scorer=xu
            )

            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c8)
            scs.score = Decimal("7.0")
            scs.comment = "The source claims to have been part of the program, but we cannot verify independently because we do not have access to Curveball. The assumption is that the BND has done the due diligence."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c9)
            scs.score = Decimal("7.0")
            scs.comment = "The source is a defector, wants to stay in Germany, and has been cooperating with the BND."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c10)
            scs.score = Decimal("4.0")
            scs.comment = "There is serious disagreement between operations personnel who doubt his credibility and WINPAC analysts who find him credible. Given the serious reservations by EUR and our lack of direct access, I have given this variable a 4."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c11)
            scs.score = Decimal("7.0")
            scs.comment = "Analysts with scientific expertise believe it is reasonable."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c12)
            scs.score = Decimal("3.0")
            scs.comment = "We only have indirect contact through the BND, which refuses direct access."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c13)
            scs.score = Decimal("3.0")
            scs.comment = "Given the dispute between case officers and analysts and the lack of direct access, there is a significant unknown unknown. "
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c14)
            scs.score = Decimal("3.0")
            scs.comment = "The ease with which a BW program can be hidden, makes it very hard to verify this claim. Part of the claim is that the mobile vehicles were used to disguise and hide the program."
            scs.save()
            add_gps(r_curveball, o)
            print("  ✓ Example Report: Curveball: Iraq Mobile WMDs")

            r_unscom, _ = Report.objects.get_or_create(
                name="Example: UNSCOM Inspector: Iraq Disarmament"
            )
            r_unscom.summary = "In June 1999 UNSCOM Inspector Ritter stated publicly that Iraq had disarmed, and in June 2000 wrote an article in Arms Control Today titled “The Case for Iraq’s Qualitative Disarmament.” United Nations weapons inspectors reported in January 2003 that they had found no indication of an active program to acquire nuclear weapons. Overall comment: The major concern is the three-year gap between when UNSCOM stated Iraq had disarmed and today. We lack the information required to explain Ritter’s flip.\n\nAnalytic Question: Is UNSCOM Inspector Ritter's claim that Iraq has disarmed its nuclear weapons program credible?"
            r_unscom.frameworks.add(f_humint)
            r_unscom.sources.add(s_unscom)
            r_unscom.feedback_score = 100
            r_unscom.save()

            sc, _ = Scorecard.objects.get_or_create(
                report=r_unscom, framework=f_humint, scorer=xu
            )

            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c8)
            scs.score = Decimal("10.0")
            scs.comment = "UNSCOM was on the ground in Iraq until 1998"
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c9)
            scs.score = Decimal("8.0")
            scs.comment = "UNSCOM was expert and professional. Ritter changed his view between August 1998 and June 1999"
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c10)
            scs.score = Decimal("5.0")
            scs.comment = "Ritter went from saying Iraq is not disarming in August 1998 to the claim above in June 1999. It is not clear why he changed his view because he resigned as an inspector in August 1998."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c11)
            scs.score = Decimal("6.0")
            scs.comment = "Yes, but the information is dated. There have been no inspectors on the ground since 1998. I rate it a 6 because three years have passed."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c12)
            scs.score = Decimal("10.0")
            scs.comment = "We have direct contact with the source. 10 for direct, face-to-face interaction, which gives the collecting entity a chance to vet and observe overtime the behavior and motivation of the source."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c13)
            scs.score = Decimal("0.0")
            scs.comment = None
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c14)
            scs.score = Decimal("7.0")
            scs.comment = "National technical means and other HUMINT can do this"
            scs.save()

            add_gps(r_unscom, o)
            print("  ✓ Example Report: UNSCOM Inspector: Iraq Disarmament")

            r_kamal, _ = Report.objects.get_or_create(
                name="Example: Kamal: Iraq Disarmament"
            )
            r_kamal.summary = "Kamal, who defected to Jordan in 1995 and cooperated with UNSCOM and Western intelligence, maintained that he had ordered the destruction of all WMD and the end to these programs after the end of the Gulf War. US officials concluded that the information Kamal provided was of limited content and value. Analysis of Hussein: Like UNSCOM, the major concern is the lengthy gap between the source’s date of information and today. Overall Analysis of HUMIT Variable: The HUMINT evidence is intriguing but not compelling one way or the other. Additional HUMINT collection or verification by the other variables is needed. Until that is available, the HUMINT must be treated with caution.\n\nAnalytic Question: Are Kamal's claims regarding the destruction of Iraq's WMD and the cessation of WMD programs credible?"
            r_kamal.sources.add(s_hussein)
            r_kamal.frameworks.add(f_humint)
            r_kamal.feedback_score = 95
            r_kamal.save()

            sc, _ = Scorecard.objects.get_or_create(
                report=r_kamal, framework=f_humint, scorer=xu
            )

            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c8)
            scs.score = Decimal("10.0")
            scs.comment = "Kamal supervised Iraq’s WMD programs starting in 1987."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c9)
            scs.score = Decimal("8.0")
            scs.comment = "Kamal defected to Jordan to flee Saddam who he feared. Although it is possible that Kamal is cooperating with Western intelligence to stay in Jordan, he has no obvious reason to make the claim that Iraq does not have an active WMD program."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c10)
            scs.score = Decimal("5.0")
            scs.comment = "Like the UNSCOM information, Kamal’s is dated. Also, US officials and others thought the information he provided was of limited value, perhaps because it could not be substantiated."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c11)
            scs.score = Decimal("6.0")
            scs.comment = "Leaving aside motivation, the claim is plausible, and is consistent with what UNSCOM claims. I rate it a 6 because seven years have passed."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c12)
            scs.score = Decimal("10.0")
            scs.comment = "Western intelligence is debriefing Kamal."
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c13)
            scs.score = Decimal("0.0")
            scs.comment = None
            scs.save()
            scs, _ = ScorecardScore.objects.get_or_create(scorecard=sc, criteria=c14)
            scs.score = Decimal("7.0")
            scs.comment = "National technical means and other HUMINT can do this\n"
            scs.save()
            add_gps(r_kamal, o)
            print("  ✓ Example Report: Kamal: Iraq Disarmament")

        print("")
        print("✓ Ox Intel setup complete.")
