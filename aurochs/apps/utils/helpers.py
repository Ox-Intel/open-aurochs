from django.urls import reverse as django_reverse
from django.utils.safestring import mark_safe


def reverse(*args, **kwargs):
    # from django_hosts.resolvers import reverse as hosts_reverse
    # kwargs["host"] = "clubhouse"
    # if "host" in kwargs:
    #     return "/%s" % hosts_reverse(*args, **kwargs).replace("://", "")
    # return hosts_reverse(*args, **kwargs).replace("://", "")
    if "host" in kwargs:
        del kwargs["host"]
    return django_reverse(*args, **kwargs)


OBJ_ORDERS = {
    "organizations": "a",
    "teams": "b",
    "users": "c",
    "tags": "ca",
    "sources": "d",
    "comments": "da",
    "criterias": "e",
    "scorecardscores": "f",
    "scorecards": "g",
    "frameworks": "h",
    "reports": "i",
    "inboxitems": "j",
    "stacks": "k",
}
REL_SPLIT_START = "__MAGIC_REL_SPLIT_START__"
REL_SPLIT_END = "__MAGIC_REL_SPLIT_END__"


def _obj_key(obj):
    if obj.startswith("window.aurochs.data."):
        object_type = obj[len("window.aurochs.data.") : obj.find("[")]
        return f"{OBJ_ORDERS[object_type]}" + obj[: obj.find("=")]
    return obj


def rel(obj, attr_name=None):
    if not obj or (attr_name is not None and not getattr(obj, attr_name)):
        return f"{REL_SPLIT_START}null{REL_SPLIT_END}"
    if obj:
        class_name = obj.__class__.__name__.lower() + "s"
        if attr_name:
            if (
                not hasattr(obj, "ox_id")
                and hasattr(obj, f"{attr_name}_id")
                and getattr(obj, attr_name)
            ):
                obj_pk = getattr(obj, f"{attr_name}_id")
                class_name = getattr(obj, attr_name).__class__.__name__.lower() + "s"
                return f"{REL_SPLIT_START}window.aurochs.data.{class_name}['{obj_pk}']{REL_SPLIT_END}"
            else:
                if hasattr(obj, attr_name) and getattr(obj, attr_name):
                    target_id = getattr(obj, attr_name).ox_id
                    class_name = (
                        getattr(obj, attr_name).__class__.__name__.lower() + "s"
                    )
                    return f"{REL_SPLIT_START}window.aurochs.data.{class_name}['{target_id}']{REL_SPLIT_END}"

        return f"{REL_SPLIT_START}window.aurochs.data.{class_name}['{obj.ox_id}']{REL_SPLIT_END}"
        # return f"{REL_SPLIT_START}window.aurochs.data.{class_name}['{obj.ox_id}']{REL_SPLIT_END}"
    else:
        return None


def rel_by_id(class_name, obj_pk):
    return (
        f"{REL_SPLIT_START}window.aurochs.data.{class_name}['{obj_pk}']{REL_SPLIT_END}"
    )
    # if not obj or (attr_name is not None and not getattr(obj, attr_name)):
    #     return f"{REL_SPLIT_START}null{REL_SPLIT_END}"
    # if obj:
    #     class_name = obj.__class__.__name__.lower() + "s"
    #     if attr_name:
    #         if (
    #             not hasattr(obj, "ox_id")
    #             and hasattr(obj, f"{attr_name}_id")
    #             and getattr(obj, attr_name)
    #         ):
    #             obj_pk = getattr(obj, f"{attr_name}_id")
    #             class_name = getattr(obj, attr_name).__class__.__name__.lower() + "s"
    #         else:
    #             if hasattr(obj, attr_name) and getattr(obj, attr_name):
    #                 target_id = getattr(obj, attr_name).ox_id
    #                 class_name = (
    #                     getattr(obj, attr_name).__class__.__name__.lower() + "s"
    #                 )
    #                 return f"{REL_SPLIT_START}window.aurochs.data.{class_name}['{target_id}']{REL_SPLIT_END}"

    #     return f"{REL_SPLIT_START}window.aurochs.data.{class_name}['{obj.ox_id}']{REL_SPLIT_END}"
    #     # return f"{REL_SPLIT_START}window.aurochs.data.{class_name}['{obj.ox_id}']{REL_SPLIT_END}"
    # else:
    #     return None


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
