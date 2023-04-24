from .base import *

DEBUG = LOCAL_SECRET["DEBUG"]

ALLOWED_HOSTS = LOCAL_SECRET["ALLOWED_HOSTS"]

WSGI_APPLICATION = "config.wsgi.local.application"
