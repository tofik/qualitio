import uuid
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
from django.conf import settings as global_settings

def settings(request):
    return {'DATE_FORMAT' : mark_safe('"%s"' %
                                      get_format('DATE_FORMAT').replace("%","").replace("y","yy"))}

def development(request):
    static_content_hash = ""
    if global_settings.DEBUG:
        static_content_hash = uuid.uuid4()

    return { "STATIC_HASH" : "?%s" % static_content_hash }
