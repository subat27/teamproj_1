from flask import Flask, Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect
import os
from datetime import datetime
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pybo.models import ConfAge
from pybo import db

mpl.rc("font", family="Malgun Gothic")

# 국내의 코로나 데이터를 연령대별로 출력하기 위해 데이터를 수정하는 코드

bp = Blueprint("age", __name__, url_prefix="/age")

@bp.route("getData")
def getData():
    

    return ""

@bp.route("/create_age_chart_img")
def init_global_data():

    covid_data_age = ConfAge.getColumnList(db.session)

    df_age = pd.DataFrame(covid_data_age)
    df_age.rename(columns={
        "deathCnt" : "사망자수", 
        "ageArea" : "연령", 
        "confCase" : "신규확진자", 
        "createDt" : "날짜"
    }, inplace=True)
    df_age["날짜"] = pd.to_datetime(df_age["날짜"])

    saveFile(df_age)

    return ""



def saveFile(df):
    filename = "age.png"
    upload_path = makedirectory()
    path = os.path.join(upload_path, filename)
    path = path.replace("\\", "/")

    plt.figure(figsize=(13, 8), layout='constrained')

    for age in df["연령"].unique():
        filter = df["연령"]==age
        plt.plot(df[filter]["날짜"], df[filter]["신규확진자"], label=age)

    plt.legend(df["연령"].unique())
    plt.savefig(path)
    plt.close()
    idx = path.find("/static/img")

    return path[idx:]

def makedirectory():
    UPLOAD_DIR="pybo/static/charts"
    name_ymd = datetime.now().strftime("%Y%m%d")

    new_dir_path = os.path.join(UPLOAD_DIR, name_ymd)

    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    return new_dir_path    
