from flask import Flask, Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect
import pandas as pd
from pybo.models import ConfLocal, ConfAge, ConfGender
from pybo import db
import os
from flask import json

bp = Blueprint("area", __name__, url_prefix="/area")

def find_data(date):
    #ConfLocal.query.order_by(ConfLocal.createDt.desc())
    return ConfLocal.query.filter_by(createDt=date).order_by(ConfLocal.createDt.desc())

@bp.route("show_data", methods=["GET", "POST"])
def show_data():
    return render_template("area/showArea.html", datasets=find_data("2020-02-08"))


