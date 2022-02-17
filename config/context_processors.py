from django.conf import settings
from django.http import HttpRequest


def google_analytics(request: HttpRequest) -> dict:
    return {
        'GOOGLE_ADSENSE_ID': settings.GOOGLE_ADSENSE_ID,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
    }
