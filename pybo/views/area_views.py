from flask import Flask, Blueprint, render_template, g, request, url_for, current_app
from werkzeug.utils import redirect
from pybo.models import ConfLocal, ConfAge, ConfGender
from pybo import db
from flask import json
from datetime import datetime
from .main_views import saveFile
from sqlalchemy import create_engine

import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
import mpld3

matplotlib.use('Agg')
plt.ioff()

bp = Blueprint("area", __name__, url_prefix="/area")

# 뭘하는 함수인 지 ex 
def find_data(date):
    #ConfLocal.query.order_by(ConfLocal.createDt.desc())
    return ConfLocal.query.filter_by(createDt=date).order_by(ConfLocal.createDt.desc())


#현황(status)라는 함수를 만들음.
@bp.route("/domestic",methods=("GET",))
def domestic():

    #현황(국내domestic)을 연결해줌
    return render_template("status/domestic.html")

@bp.route("/overseas",methods=("GET",))
def overseas():

    #현황(해외domestic)을 연결해줌
    return render_template("status/overseas.html")

@bp.route("/canada", methods=("GET",))
def canada():
    return render_template("overseas/canada.html")



@bp.route("show_data", methods=["GET", "POST"])
def show_data():
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    data = pd.read_sql("select * from ConfLocal where localNameEn='Gwangju'", engine)

    saveFile(data, "Gwangju")

    return render_template("area/showArea.html", datasets=find_data("2020-02-08"))


