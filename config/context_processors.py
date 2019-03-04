from django.conf import settings


def google_analytics(request):
    return {
        'GOOGLE_ADSENSE_ID': settings.GOOGLE_ADSENSE_ID,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
    }
