from flask import Blueprint, render_template, request
from werkzeug.utils import redirect
from pybo.models import Country
from pybo import db
import pandas as pd
from datetime import datetime
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

bp = Blueprint("overseas", __name__, url_prefix="/overseas")

# 해외의 코로나 데이터를 출력하기 위해 데이터를 수정하는 코드

@bp.route("/graph")
def overseas_graph():
    country = Country.query.all()
    filepath_date = datetime.now().strftime("%Y%m%d")
    
    return render_template("overseas/overseas_graph.html", country=country, filepath_date=filepath_date)

@bp.route("/detail/<country>")
def detail(country):
    countryData = Country.query.filter_by(name=country).get()
    return render_template("", countryData=countryData)

# 국가를 입력하면 화면에 그 국가에 대한 정보가 나타나게 구현
@bp.route("/find/<country>", methods=('GET', 'POST'))
def db_input():
    if request.method == "GET" :
        return render_template("country_input.html")
    
    country = request.form["country"]
    
    return render_template("overseas/detail/" + country)


@bp.route("/initDB")
def db_input2():
    df = pd.read_csv("pybo\static\data\COVID19-global.csv")

    df1 = df.copy()
    df1 = df1.drop(columns=df1.columns[[1, 3, 5, 6, 7]])
    df1.rename(columns={'Date_reported':'날짜',
                        'Country':'국가',
                        'New_cases':'감염자'}, inplace=True)
    df1["날짜"] = pd.to_datetime(df1["날짜"])
    
    # 240국가를 db에 저장해주는 코드 ######
    for name in df1["국가"].unique():
        country = Country(name=name)
        db.session.add(country)

    db.session.commit()

    return redirect("/")

# 해외 데이터를 이미지화한 파일을 저장하는 함수
@bp.route("createImgFile")
def init_overseas_data():
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

    return redirect("/")


def saveFile(df, area):
    filename = area + ".png"
    upload_path = makedirectory()
    path = os.path.join(upload_path, filename)
    path = path.replace("\\", "/")

    filter=df["국가"]==area 
    temp_df = df[filter]
    temp_df.plot(x="날짜", y=["신규확진자"])
    plt.savefig(path)
    plt.close()

    idx = path.find("/static/img")

    return path[idx:]

def makedirectory():
    UPLOAD_DIR="pybo/static/img"
    name_ymd = datetime.now().strftime("%Y%m%d")

    new_dir_path = os.path.join(UPLOAD_DIR, name_ymd)

    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    return new_dir_path
 