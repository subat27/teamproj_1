from flask import Flask, Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect

bp = Blueprint("age", __name__, url_prefix="/age")

