from django import template
from base64 import b64encode
from functools import reduce
import math
import random
import string
import statistics
import json
from django.utils.safestring import mark_safe

# Copy from tailwind.config.js (not DRY, keep these synced.)
CHART_COLORS = [
    "hsl(251,32.7%,41.4%)",
    "hsl(207,55.6%,38.8%)",
    "hsl(191,95.3%,33.7%)",
    "hsl(172,86.5%,37.6%)",
    "hsl(158,81.7%,47.3%)",
    "hsl(113,65.9%,67.8%)",
    "hsl(82,72.4%,65.9%)",
    "hsl(58,82.3%,64.5%)",
    "hsl(43,84.9%,63.5%)",
    "hsl(30,86.5%,62.4%)",
    "hsl(251,22.7%,31.4%)",
    "hsl(207,45.6%,28.8%)",
    "hsl(191,85.3%,23.7%)",
    "hsl(172,76.5%,27.6%)",
    "hsl(158,71.7%,37.3%)",
    "hsl(113,55.9%,57.8%)",
    "hsl(82,62.4%,55.9%)",
    "hsl(58,72.3%,54.5%)",
    "hsl(43,74.9%,53.5%)",
    "hsl(30,76.5%,52.4%)",
    "hsl(251,32.7%,41.4%)",
    "hsl(207,55.6%,38.8%)",
    "hsl(191,95.3%,33.7%)",
    "hsl(172,86.5%,37.6%)",
    "hsl(158,81.7%,47.3%)",
    "hsl(113,65.9%,67.8%)",
    "hsl(82,72.4%,65.9%)",
    "hsl(58,82.3%,64.5%)",
    "hsl(43,84.9%,63.5%)",
    "hsl(30,86.5%,62.4%)",
    "hsl(251,32.7%,21.4%)",
    "hsl(207,55.6%,28.8%)",
    "hsl(191,95.3%,23.7%)",
    "hsl(172,86.5%,27.6%)",
    "hsl(158,81.7%,37.3%)",
    "hsl(113,65.9%,47.8%)",
    "hsl(82,72.4%,45.9%)",
    "hsl(58,82.3%,44.5%)",
    "hsl(43,84.9%,43.5%)",
    "hsl(30,86.5%,42.4%)",
    "hsl(251,32.7%,41.4%)",
    "hsl(207,55.6%,38.8%)",
    "hsl(191,95.3%,33.7%)",
    "hsl(172,86.5%,37.6%)",
    "hsl(158,81.7%,47.3%)",
    "hsl(113,65.9%,67.8%)",
    "hsl(82,72.4%,65.9%)",
    "hsl(58,82.3%,64.5%)",
    "hsl(43,84.9%,63.5%)",
    "hsl(30,86.5%,62.4%)",
    "hsl(251,22.7%,31.4%)",
    "hsl(207,45.6%,28.8%)",
    "hsl(191,85.3%,23.7%)",
    "hsl(172,76.5%,27.6%)",
    "hsl(158,71.7%,37.3%)",
    "hsl(113,55.9%,57.8%)",
    "hsl(82,62.4%,55.9%)",
    "hsl(58,72.3%,54.5%)",
    "hsl(43,74.9%,53.5%)",
    "hsl(30,76.5%,52.4%)",
    "hsl(251,32.7%,41.4%)",
    "hsl(207,55.6%,38.8%)",
    "hsl(191,95.3%,33.7%)",
    "hsl(172,86.5%,37.6%)",
    "hsl(158,81.7%,47.3%)",
    "hsl(113,65.9%,67.8%)",
    "hsl(82,72.4%,65.9%)",
    "hsl(58,82.3%,64.5%)",
    "hsl(43,84.9%,63.5%)",
    "hsl(30,86.5%,62.4%)",
    "hsl(251,32.7%,21.4%)",
    "hsl(207,55.6%,18.8%)",
    "hsl(191,95.3%,13.7%)",
    "hsl(172,86.5%,17.6%)",
    "hsl(158,81.7%,27.3%)",
    "hsl(113,65.9%,47.8%)",
    "hsl(82,72.4%,45.9%)",
    "hsl(58,82.3%,44.5%)",
    "hsl(43,84.9%,43.5%)",
    "hsl(30,86.5%,42.4%)",
]

register = template.Library()


cachedSeeds = {}


def hashToInt(seed):
    num = ""
    for c in seed:
        num += str(ord(c))

    # print(num)
    return int(num)


def seeded_random(seed):
    if seed in cachedSeeds:
        return cachedSeeds[seed]

    random.seed(hashToInt(seed))
    rand = random.random()
    # print(rand)
    cachedSeeds[seed] = rand
    return rand


def get_avatar_color(user, index=None):
    colors = [
        "hsl(200, 30%, 80%)",
        "hsl(200, 30%, 70%)",
        "hsl(200, 30%, 60%)",
        "hsl(200, 30%, 50%)",
        "hsl(200, 30%, 40%)",
        "hsl(200, 30%, 30%)",
        "hsl(200, 30%, 20%)",
        "hsl(225, 30%, 80%)",
        "hsl(225, 30%, 70%)",
        "hsl(225, 30%, 60%)",
        "hsl(225, 30%, 50%)",
        "hsl(225, 30%, 40%)",
        "hsl(225, 30%, 30%)",
        "hsl(225, 30%, 20%)",
        "hsl(180, 30%, 80%)",
        "hsl(180, 30%, 70%)",
        "hsl(180, 30%, 60%)",
        "hsl(180, 30%, 50%)",
        "hsl(180, 30%, 40%)",
        "hsl(180, 30%, 30%)",
        "hsl(180, 30%, 20%)",
    ]

    # idx = math.floor(seeded_random(seed) * len(colors))

    if index or index == 0:
        return colors[index]
    return colors[user.color_index]


def get_avatar_color_by_index(index):
    colors = [
        "hsl(200, 30%, 80%)",
        "hsl(200, 30%, 70%)",
        "hsl(200, 30%, 60%)",
        "hsl(200, 30%, 50%)",
        "hsl(200, 30%, 40%)",
        "hsl(200, 30%, 30%)",
        "hsl(200, 30%, 20%)",
        "hsl(225, 30%, 80%)",
        "hsl(225, 30%, 70%)",
        "hsl(225, 30%, 60%)",
        "hsl(225, 30%, 50%)",
        "hsl(225, 30%, 40%)",
        "hsl(225, 30%, 30%)",
        "hsl(225, 30%, 20%)",
        "hsl(180, 30%, 80%)",
        "hsl(180, 30%, 70%)",
        "hsl(180, 30%, 60%)",
        "hsl(180, 30%, 50%)",
        "hsl(180, 30%, 40%)",
        "hsl(180, 30%, 30%)",
        "hsl(180, 30%, 20%)",
    ]

    # idx = math.floor(seeded_random(seed) * len(colors))
    return colors[index]


@register.filter(name="json")
def json_filter(value):
    return mark_safe(json.dumps(value))


@register.filter(name="times")
def times(number):
    return range(1, number + 1)


@register.filter(name="dict_key")
def dict_key(d, k):
    if d and (hasattr(d, k) or k in d):
        if hasattr(d, k):
            return getattr(d, k)

        return d[k]
    return None


@register.filter
def multiply(value, arg):
    return float(value) * float(arg)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def add_float(value, arg):
    return float(value) + float(arg)


@register.simple_tag
def htb_content():
    choices = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(
        random.SystemRandom().choice(choices)
        for i in range(round(random.random() * 2000))
    )


def getCriteriaColor(index):
    global CHART_COLORS
    return CHART_COLORS[index]


@register.simple_tag
def criteria_color(index):
    return getCriteriaColor(index)


@register.simple_tag
def criteria_color_outline(index):
    return getCriteriaColor(index).replace("hsl", "hsla").replace("%)", "%, 0.5)")


def getRotatedCoordinates(x, y, rotation, radius, offset):
    # Need to convert the X and Y to where they'd be rotated x degrees.
    normalized_rotation = (float(rotation) / 100.0) - 0.25

    rotated_y = math.sin(normalized_rotation * 2 * math.pi) * radius
    rotated_x = math.cos(normalized_rotation * 2 * math.pi) * radius
    rotated_x = rotated_x + offset
    rotated_y = rotated_y + offset

    ret = f"{rotated_x} {rotated_y}"

    return ret


def getArcPath(all_criteria, target_criteria):
    rotation = 0
    for c in all_criteria:
        if c.id == target_criteria.id:
            break
        else:
            rotation += c.relative_weight_as_percent

    # We're in a 42x42 space.
    arcDepth = 8
    center = 21
    outerRadius = center
    innerRadius = center - arcDepth
    arcAngle = target_criteria.relative_weight_as_percent

    # This works by just thinking about each operation on the y-axis, and then "moving" the pointer with the
    # rotation parameter.  Make sure your radius is right, and things should JustWork TM.
    return (
        f"M {getRotatedCoordinates(0, -1 * innerRadius, rotation, innerRadius, center)}"
        + f"L {getRotatedCoordinates(-1 * innerRadius, -1 * outerRadius, rotation, outerRadius, center)}"
        + f"A {outerRadius}, {outerRadius}, 0, 0, 1, {getRotatedCoordinates(0, -1 * outerRadius, rotation + arcAngle, outerRadius, center)}"  # noqa
        + f"L {getRotatedCoordinates(0, -1 * innerRadius, rotation + arcAngle, innerRadius, center)}"
        + f"A {innerRadius}, {innerRadius}, 0, 0, 0, {getRotatedCoordinates(0, -1 * innerRadius, rotation, innerRadius, center)}"
    )


@register.simple_tag
def render_donut_chart(framework):
    out_str = '<svg height="100%" width="100%" viewBox="0 0 42 42">'
    for c in framework.criteria:
        out_str += f"""<path d="{getArcPath(framework.criteria, c)}" fill="{getCriteriaColor(c.index)}"/>"""
    out_str += "</svg>"
    # return out_str
    return mark_safe(out_str)
    # print(out_str.encode("utf-8"))
    # return mark_safe("data:image/svg+xml;charset=utf-8;base64," + b64encode(out_str.encode("utf-8")))


@register.simple_tag
def weight_circle_css(c):
    w = float(c.weight)
    if w >= 9:
        padding_str = f"{ w * 1.0}px { w * 1.1}px { w * 0.6}px { w * 1.1}px"
    else:
        padding_str = f"{ w * 1.0}px { w * 1.1}px { w * 0.6}px { w * 1.1}px"

    ret = f"padding: {padding_str}; width: 24px; margin: {18-w}px auto 0px auto; "
    ret += (
        f"line-height: 1.5em; vertical-align: middle; font-size: { 1 + (0.02 * w) }em;"
    )
    # print(ret)
    return ret


@register.simple_tag
def noise_badge(stddev):
    if stddev < 0:
        # return mark_safe("")
        badge_text = "n/a"
    elif stddev > 2.25:
        badge_text = "high"
    elif stddev > 1.2:
        badge_text = "medium"
    else:
        badge_text = "low"

    return mark_safe(
        f"""<div class="badge_container"><div class="badge {badge_text}">{badge_text}</div></div>"""
    )


@register.simple_tag
def noise_badge_skip_na(stddev):
    if stddev < 0:
        return mark_safe("")
        # badge_text = "n/a"
    elif stddev > 2.25:
        badge_text = "high noise"
    elif stddev > 1.2:
        badge_text = "medium noise"
    else:
        badge_text = "low noise"

    return mark_safe(
        f"""<div class="badge_container"><div class="badge {badge_text}">{badge_text}</div></div>"""
    )


@register.simple_tag
def noise_badge_skip_na_do_calc(target_scs, stack):
    scores = []
    for r in stack.authorized_reports:
        for sc in r.scorecards:
            for scs in sc.scores:
                if scs.score is not None and scs.criteria.pk == target_scs.criteria.pk:
                    scores.append(scs.score)
    if len(scores) < 2:
        return mark_safe("")
    stddev = statistics.stdev(scores)

    if stddev < 0:
        return mark_safe("")
        # badge_text = "n/a"
    elif stddev > 2.25:
        badge_text = "high noise"
    elif stddev > 1.2:
        badge_text = "medium noise"
    else:
        badge_text = "low noise"

    return mark_safe(
        f"""<div class="badge_container"><div class="badge {badge_text}">{badge_text}</div></div>"""
    )


@register.simple_tag
def noise_badge_skip_na_do_calc_report(target_scs, stack):
    scores = []
    for r in stack.authorized_reports:
        for sc in r.scorecards:
            for scs in sc.scores:
                if (
                    scs.score is not None
                    and scs.criteria.pk == target_scs.criteria.pk
                    and scs.scorecard.report == target_scs.scorecard.report
                ):
                    scores.append(scs.score)
    if len(scores) < 2:
        return mark_safe("")
    stddev = statistics.stdev(scores)

    if stddev < 0:
        return mark_safe("")
        # badge_text = "n/a"
    elif stddev > 2.25:
        badge_text = "high noise"
    elif stddev > 1.2:
        badge_text = "medium noise"
    else:
        badge_text = "low noise"

    return mark_safe(
        f"""<div class="badge_container"><div class="badge {badge_text}">{badge_text}</div></div>"""
    )


@register.simple_tag
def framework_report_ox_score(framework, report):
    return round(framework.report_ox_score(report))


@register.simple_tag
def framework_stack_ox_score(framework, stack):
    return round(framework.stack_ox_score(stack))


@register.simple_tag
def get_scored_criteria(stack, criteria):
    return {}
    # return round(framework.stack_ox_score(stack))


@register.simple_tag
def max_stack_offset(sbc):
    scores_per_value = {}
    for scs in sbc["scores"]:
        if f"{scs.score}" not in scores_per_value:
            scores_per_value[f"{scs.score}"] = []
        scores_per_value[f"{scs.score}"].append(scs)

    max_stack = 0
    for k, v in scores_per_value.items():
        if len(v) > max_stack:
            max_stack = len(v)

    return max_stack * 20


@register.simple_tag
def max_stack_offset_report(sbc):
    # for sc in c.scorecard.report:
    #     for scs in sc.scores:
    #         if scs.critera.pk == c.pk
    scores_per_value = {}
    for scs in sbc["scores"]:
        if f"{scs['average']}" not in scores_per_value:
            scores_per_value[f"{scs['average']}"] = []
        scores_per_value[f"{scs['average']}"].append(scs)

    max_stack = 0
    for k, v in scores_per_value.items():
        if len(v) > max_stack:
            max_stack = len(v)

    return max_stack * 20


@register.simple_tag
def max_stack_offset_report_header(sbc):
    # Just don't even ask.  I'm sorry.
    # for sc in c.scorecard.report:
    #     for scs in sc.scores:
    #         if scs.critera.pk == c.pk
    scores_per_value = {}
    for scs in sbc["scores"]:
        if f"{scs['average']}" not in scores_per_value:
            scores_per_value[f"{scs['average']}"] = []
        scores_per_value[f"{scs['average']}"].append(scs)

    max_stack = 0
    for k, v in scores_per_value.items():
        if len(v) > max_stack:
            max_stack = len(v)

    return 20 + (max_stack * 25)


@register.simple_tag
def dot_plot_score(sbc):
    if len(sbc["scores"]) == 0:
        return mark_safe('<div class="no_scores">No Scores</div>')

    out_str = """<div class="dot_plot">
            <div class="line"></div>"""

    out_str += f"""<div class="average_line" style="left: {float(sbc["average"]) * 10}%" ></div>"""

    scores_per_value = {}
    for scs in sbc["scores"]:
        if f"{scs.score}" not in scores_per_value:
            scores_per_value[f"{scs.score}"] = []
        top = 10 + (len(scores_per_value[f"{scs.score}"]) * -20)
        scores_per_value[f"{scs.score}"].append(scs)

        out_str += f"""<div class="dot" style="top: {top}px; left: { float(scs.score) * 10}%">{round(scs.score)}</div>"""

    max_stack = 0
    for k, v in scores_per_value.items():
        if len(v) > max_stack:
            max_stack = len(v)

    out_str = (
        f"""<div class="dot_plot" style="bottom: {max_stack  * 0}px; ">"""
        + out_str
        + "</div>"
    )
    # print(out_str)
    return mark_safe(out_str)


@register.simple_tag
def dot_plot_initial(sbc):
    if len(sbc["scores"]) == 0:
        return mark_safe('<div class="no_scores absolute">No Scores</div>')

    out_str = """<div class="line"></div>"""

    out_str += f"""<div class="average_line" style="left: {float(sbc["average"]) * 10}%" ></div>"""
    scores_per_value = {}
    for scs in sbc["scores"]:
        if f"{scs.score}" not in scores_per_value:
            scores_per_value[f"{scs.score}"] = []
        top = 10 + (len(scores_per_value[f"{scs.score}"]) * -20)
        scores_per_value[f"{scs.score}"].append(scs)
        color = get_avatar_color(scs.scorecard.scorer)
        out_str += f"""<div class="dot" style="top: {top}px; background-color: {color}; left: { float(scs.score) * 10}%">{scs.scorecard.scorer.full_name[:1]}</div>"""  # noqa

    max_stack = 0
    for k, v in scores_per_value.items():
        if len(v) > max_stack:
            max_stack = len(v)

    out_str = (
        f"""<div class="dot_plot" style="bottom: {max_stack  * 0}px; ">"""
        + out_str
        + "</div>"
    )
    # print(out_str)
    return mark_safe(out_str)


@register.simple_tag
def dot_plot_report(stack, criteria, sbc):
    # print(stack)
    # print(criteria)
    # print(sbc)

    averages = []
    found_scores = False
    scores_per_report = {}
    for report in stack.authorized_reports:
        if report.ox_id not in scores_per_report:
            scores_per_report[report.ox_id] = []
        for sc in report.scorecards:
            for scs in sc.scores:
                if scs.criteria == criteria and scs.score is not None:
                    found_scores = True
                    # if f"{scs.score}" not in scores_per_report[report.ox_id]:
                    #     scores_per_report[report.ox_id][f"{scs.score}"] = []
                    scores_per_report[report.ox_id].append(scs)

    if not found_scores:
        return mark_safe('<div class="no_scores absolute">No Scores</div>')

    scores_per_value = {}
    for report_id, report_scores in scores_per_report.items():
        total = 0
        num = 0
        for scs in report_scores:
            total += scs.score
            num += 1
        if num > 0:
            average = total / num
            scs.average = average
            if f"{average}" not in scores_per_value:
                scores_per_value[f"{average}"] = []
            scores_per_value[f"{average}"].append(scs)
            averages.append(average)

    out_str = """<div class="line"></div>"""
    max_stack = 0
    for value, scores in scores_per_value.items():
        top_count = 0
        for scs in scores:
            top = 27 + (len(scores) * -20) + (20 * top_count)
            color = get_avatar_color(None, index=scs.scorecard.report.color_index)
            out_str += f"""<div class="dot" style="top: {top}px; background-color: {color}; left: { float(scs.average) * 10}%">{scs.scorecard.report.name[:2]}</div>"""  # noqa
            top_count += 1
            if top_count > max_stack:
                max_stack = top_count

    found_scores = False
    for report in stack.authorized_reports:
        if len(report.scorecards) > 0:
            found_scores = True
            break

    # if not found_scores:
    #     return mark_safe('<div class="no_scores absolute">No Scores</div>')

    # out_str = """<div class="line"></div>"""

    # scores_per_value = {}
    # averages = []
    # for report in stack.authorized_reports:
    #     report_criteria_scs = None
    #     for r_id, scs in sbc.items():
    #         if scs["report"] == report and scs["criteria"] == criteria:
    #             break

    #     if f"{scs['average']}" not in scores_per_value:
    #         scores_per_value[f"{scs['average']}"] = []
    #     top = 10 + (len(scores_per_value[f"{scs['average']}"]) * -20)
    #     scores_per_value[f"{scs['average']}"].append(scs)
    #     averages.append(scs["average"])
    #     color = get_avatar_color(None, index=report.color_index)
    #     out_str += f"""<div class="dot" style="top: {top}px; background-color: {color}; left: { float(scs["average"]) * 10}%">{scs["report"].name[:2]}</div>"""  # noqa

    # max_stack = 0
    # for k, v in scores_per_value.items():
    #     if len(v) > max_stack:
    #         max_stack = len(v)

    avg_line = ""
    if len(averages) > 0:
        avg_line = f"""<div class="average_line" style="left: {float(sum(averages) / len(averages)) * 10}%" ></div>"""

    out_str = (
        f"""<div class="report_plot" style="bottom: {max_stack  * 0}px; ">"""
        + avg_line
        + out_str
        + "</div>"
    )
    # print(out_str)
    return mark_safe(out_str)


@register.simple_tag
def dot_plot_single(score):
    out_str = """<div class="dot_plot">
            <div class="line"></div>"""

    out_str += f"""<div class="dot" style="left: { float(score) * 10}%">{score}</div>"""

    out_str += "</div>"
    return mark_safe(out_str)


@register.simple_tag
def avatar_color(user):
    return get_avatar_color(user)


@register.simple_tag
def avatar_color_by_index(user):
    return get_avatar_color_by_index(user)


@register.simple_tag
def get_report_average_score(target_scs):
    all_scores = 0
    num_scores = 0
    for sc in target_scs.scorecard.report.scorecards:
        for scs in sc.scores:
            if scs.criteria.pk == target_scs.criteria.pk and scs.score is not None:
                all_scores += scs.score
                num_scores += 1
    if num_scores > 0:
        return 10 * all_scores / num_scores
    return 0
