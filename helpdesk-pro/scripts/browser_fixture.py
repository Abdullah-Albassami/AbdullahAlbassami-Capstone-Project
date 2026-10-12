"""Disposable browser-verification server; refuses any existing database."""

import os
from pathlib import Path
import sys
from io import StringIO
from wsgiref.simple_server import make_server, WSGIRequestHandler

APP_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_DIR))
database = Path(os.environ["HELPDESK_BROWSER_DB"]).resolve()
if database.exists() or not database.parent.name.startswith("helpdesk-browser-"):
    raise RuntimeError("Browser verification requires a new database in its own temporary directory.")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from django.conf import settings

settings.DATABASES["default"]["NAME"] = str(database)
import django

django.setup()
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

call_command("migrate", verbosity=0)
call_command("seed_demo", stdout=StringIO())
User.objects.create_superuser("browser_setup", password=os.environ["DEMO_PASSWORD"])


class QuietHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        pass


with make_server("127.0.0.1", 0, StaticFilesHandler(get_wsgi_application()), handler_class=QuietHandler) as server:
    print(server.server_port, flush=True)
    server.serve_forever()
