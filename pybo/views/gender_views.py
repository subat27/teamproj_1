from flask import Flask, Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect
import os
from datetime import datetime
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pybo.models import ConfGender
from pybo import db

bp = Blueprint("gender", __name__, url_prefix="/gender")

# 국내의 코로나 데이터를 성별로 출력하기 위해 데이터를 수정하는 코드

@bp.route("getData")
def getData():
    

    return ""


@bp.route("/create_gender_chart_img")
def init_global_data():
    
    covid_data_gender = ConfGender.getColumnList(db.session)

    df_gender = pd.DataFrame(covid_data_gender)
    df_gender.rename(columns={
        "deathCnt" : "사망자수", 
        "gender" : "성별", 
        "confCase" : "신규확진자", 
        "createDt" : "날짜"
    }, inplace=True)
    df_gender["날짜"] = pd.to_datetime(df_gender["날짜"])

    saveFile(df_gender)

    return ""



def saveFile(df):
    filename = "gender.png"
    upload_path = makedirectory()
    path = os.path.join(upload_path, filename)
    path = path.replace("\\", "/")

    plt.figure(figsize=(13, 8), layout='constrained')

    for gender in df["성별"].unique():
        filter = df["성별"]==gender
        plt.plot(df[filter]["날짜"], df[filter]["신규확진자"], label=gender)

    plt.legend(df["성별"].unique())
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

