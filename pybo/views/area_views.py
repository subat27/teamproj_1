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

    #날짜 입력받아서 날짜에 해당하는 값 찾아줌

    return ConfLocal.query.filter_by(createDt=date).all()

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



