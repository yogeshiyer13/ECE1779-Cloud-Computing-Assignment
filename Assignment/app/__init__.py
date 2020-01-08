from flask import Flask

webapp = Flask(__name__)

webapp.secret_key = "aT\x18\xc0F\xe4\xb3\x04L\x1fjf}\x8bt\xdf\x9b\x9e\xbaV\x18|\xb2\xcc"

from app import main
from app import images
from app import routes

