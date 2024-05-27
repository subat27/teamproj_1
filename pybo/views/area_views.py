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


from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpld3
plt.ioff()

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

@bp.route("test")
def test():
    df = pd.read_csv("pybo\static\data\covid_data_korea_local.csv")
    
    df1 = df[['gubun', 'deathCnt', 'defCnt', 'stdDay', 'incDec', 'gubunEn']]
    df1 = df1.loc[(df["gubun"]!="합계")&(df["gubun"]!="검역")]
    df1.drop_duplicates(subset=["gubun", "stdDay"], inplace=True)
    df1.reset_index(inplace=True)
    df1.drop(columns=["index"], inplace=True)
    df1["stdDay"] = pd.to_datetime(df1["stdDay"])

    covid_data_local = df1.copy().sort_values(by=["stdDay", "gubunEn"])

    #covid_data_local = df[['gubun', 'deathCnt', 'defCnt', 'stdDay', 'incDec', 'gubunEn']].loc[(df["gubun"]!="합계")&(df["gubun"]!="검역")].drop_duplicates(subset=["gubun", "stdDay"]).reset_index().drop(columns=["index"])
    data_link = saveFile(covid_data_local, "Jeju")
   
    return render_template("index.html", data_link=data_link)


def saveFile(df, area):
    filename = area + ".html"
    upload_path = makedirectory()

    path = os.path.join(upload_path, filename)
    path = path.replace("\\", "/")
    
    if not checkFile(path):
        temp_df = df.loc[df["gubunEn"]==area]

        fig = plt.figure(figsize=(8, 4), layout='constrained')
        plt.plot(temp_df['stdDay'], temp_df['defCnt'])
        plt.xlabel('stdDay')
        plt.ylabel('confCase')
        html_graph = mpld3.fig_to_html(fig)

        with open(path, "w") as f:
            f.write(html_graph)

    idx = path.find("/static/charts")

    return path[idx:]

def makedirectory():
    UPLOAD_DIR="pybo/static/charts"
    name_ymd = datetime.now().strftime("%Y%m%d")

    new_dir_path = os.path.join(UPLOAD_DIR, name_ymd)

    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    return new_dir_path

def checkFile(path):
    if os.path.exists(path):
        return True

    return False




