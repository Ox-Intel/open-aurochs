import os
import datetime
import time

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Resets the dev database"

    def add_arguments(self, parser):
        parser.add_argument("--confirm", type=bool)

    def handle(self, *args, **options):
        dir_path = os.path.join(
            settings.APPS_DIR, "webapp", "templates", "webapp", "guide"
        )
        with open(
            os.path.join(
                dir_path,
                "Getting started with Ox 46c4e3edb17f4b52a9468e1c51f08c60.html",
            ),
            "r",
        ) as f:
            content = f.read()
            titles = []
            page_delimiter = '<li style="list-style-type:disc"><mark class="highlight-purple"><a href="Getting%20started%20with%20Ox%2046c4e3edb17f4b52a9468e1c51f08c60.html">'  # noqa
            partials = content.split(page_delimiter)
            first = True
            for p in partials:
                if first:
                    first = False
                else:
                    end = p.find("</a>")
                    if end != -1:
                        title_name = p[:end].strip()
                        titles.append(title_name)
                        print(title_name)
            page_delimiter = '<a href="Getting%20started%20with%20Ox%2046c4e3edb17f4b52a9468e1c51f08c60.html"><mark class="highlight-purple">'  # noqa
            partials = content.split(page_delimiter)
            first = True
            for p in partials:
                if first:
                    first = False
                else:
                    end = p.find("</mark>")
                    if end != -1:
                        title_name = p[:end].strip()
                        titles.append(title_name)
                        print(title_name)

            titles_to_ids = {}
            #  Go through a
            partials = content.split("<h2")
            for p in partials:
                partial_title_end = p.find("</h2>")
                if partial_title_end != -1:
                    partial_title = p[:partial_title_end].lower()
                    for t in titles:
                        if partial_title.find(t.lower()) != -1:
                            id_start = p.find('id="') + 4
                            id_end = p.find('"', id_start)
                            id = p[id_start:id_end]
                            titles_to_ids[t] = id

            body_content_start_idx = content.find(
                '<hr id="e180b712-9fd6-4721-bb90-0cb5322a2d48"/>'
            )
            body_content_end_idx = content.find("</div></div></article></body></html>")
            body_content = content[
                body_content_start_idx
                + len(
                    '<hr id="e180b712-9fd6-4721-bb90-0cb5322a2d48"/>'
                ) : body_content_end_idx
            ]
            body_content_lower = body_content.lower()

            titles.sort(key=lambda x: body_content_lower.find(x))
        # Then cut from
        # <p id="d92c8d81-2f19-4829-9327-341a96ded1b5" class="">
        #  to
        # </div></div></article></body></html>
        # and keep it.

        drawer_content = ""
        for t in titles:
            id = titles_to_ids[t]
            drawer_content += f"<li><a href='#{id}'>{t}</a></li>\n"

        output_content = f"""
<div class="drawer drawer-mobile">
  <div class="drawer-content flex flex-col items-center justify-center">
    {body_content}
  </div>
  </div>
  <div class="drawer-side">
    <label for="my-drawer-2" class="drawer-overlay"></label>
    <ul class="menu p-4 w-80 bg-base-100 text-base-content">
    {drawer_content}
    </ul>
  </div>
</div>
        """

        # print(output_content)
        dir_path = os.path.join(settings.APPS_DIR, "webapp", "src", "pages")
        with open(os.path.join(dir_path, "GuidePage.vue"), "r") as f:
            guide_contents = f.read()
            # print(guide_contents)
            template_start = "<!-- Start guide template  -->"
            template_end = "<!-- End guide template  -->"

            new_guide = ""
            new_guide += (
                guide_contents[: guide_contents.find(template_start)] + template_start
            )
            new_guide += output_content + "\n"
            new_guide += guide_contents[guide_contents.find(template_end) :]
            new_guide = new_guide.replace(" ", " ")
            # print(new_guide)
        with open(os.path.join(dir_path, "GuidePage.vue"), "w+") as f:
            f.write(new_guide)
        # Then assemble the page within the template.
