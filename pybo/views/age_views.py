from flask import Flask, Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect
import os
from datetime import datetime
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc("font", family="Malgun Gothic")

bp = Blueprint("age", __name__, url_prefix="/age")

@bp.route("/init_global_data")
def init_global_data():
    df = pd.read_csv("pybo\static\data\COVID19-global.csv")

    df1 = df.copy()
    df1=df1.drop(columns=df1.columns[[1, 3, 6, 7]])

    df1.rename(columns={'Date_reported':'날짜',
                        'Country':'국가',
                        'New_cases':'신규확진자',
                        'Cumulative_cases':'누적확진자'}, inplace=True)

    df1["날짜"] = pd.to_datetime(df1["날짜"])
       
    for area in df1["국가"].unique():
        saveFile(df1, area)

    return redirect("")


def saveFile(df, area):
    filename = area + ".png"
    upload_path = makedirectory()
    path = os.path.join(upload_path, filename)
    path = path.replace("\\", "/")

    filter=df["국가"]==area 
    temp_df = df[filter]
    temp_df.plot(x="날짜", y=["신규확진자"])
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
