from flask import Flask, Blueprint, render_template, g, request, url_for, current_app
from werkzeug.utils import redirect
import pandas as pd
from pybo.models import ConfLocal, ConfAge, ConfGender
from pybo import db
import os
from flask import json
from .main_views import saveFile
from datetime import datetime
from sqlalchemy import create_engine



bp = Blueprint("area", __name__, url_prefix="/area")

def find_data(date):
    #ConfLocal.query.order_by(ConfLocal.createDt.desc())
    return ConfLocal.query.filter_by(createDt=date).order_by(ConfLocal.createDt.desc())

@bp.route("show_data", methods=["GET", "POST"])
def show_data():
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    data = pd.read_sql("select * from ConfLocal where localNameEn='Gwangju'", engine)

    saveFile(data, "Gwangju")

    return render_template("area/showArea.html", datasets=find_data("2020-02-08"))


