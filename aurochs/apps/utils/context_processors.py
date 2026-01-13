from django.conf import settings


def is_debug(context):
    return {
        "IS_DEBUG": settings.DEBUG is True,
        "AIRGAPPED": settings.AIRGAPPED is True,
        "AUROCHS_DOMAIN": settings.AUROCHS_DOMAIN,
        "PAGE_URL": context.build_absolute_uri(context.get_full_path()).replace(
            "http://", "https://"
        ),
        "PAGE_DOMAIN": context.build_absolute_uri("/")[:-1],
        "WS_DOMAIN": context.build_absolute_uri("/")[:-1].replace("http", "ws"),
    }
