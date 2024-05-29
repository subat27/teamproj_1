from flask import Flask, Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect
import os
from datetime import datetime
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

bp = Blueprint("age", __name__, url_prefix="/age")

@bp.route("/show")
def show():
    # filter = df["국가명"]==nation
    # df[filter].plot().save_fig()  데이터프레임을 html/png 파일로 저장

    mpl.rc("font", family="Malgun Gothic")

    df = pd.read_csv("pybo\static\data\COVID19-global.csv")

    df1 = df.copy()
    df1=df1.drop(columns=df1.columns[[1, 3, 5, 6, 7]])

    df1.rename(columns={'Date_reported':'날짜',
                        'Country':'국가',
                        'New_cases':'감염자'}, inplace=True)

    df1["날짜"] = pd.to_datetime(df1["날짜"])
       
    for area in df1["국가"].unique():
        saveFile(df1, area)

    return render_template("")


def saveFile(df, area):
    filename = area + ".png"
    upload_path = makedirectory()
    path = os.path.join(upload_path, filename)
    path = path.replace("\\", "/")

    filter=df["국가"]==area 
    temp_df = df[filter]
    temp_df.plot(x="날짜", y=["감염자"])
    plt.savefig(path)

    idx = path.find("/static/img")

    return path[idx:]

def makedirectory():
    UPLOAD_DIR="pybo/static/img"
    name_ymd = datetime.now().strftime("%Y%m%d")

    new_dir_path = os.path.join(UPLOAD_DIR, name_ymd)

    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    return new_dir_path
