from django.conf import settings


def environment_type(request):
    return {
        'IS_DEV': settings.IS_DEV,
        'IS_TEST': settings.IS_TEST,
        'IS_PROD': settings.IS_PROD,
    }