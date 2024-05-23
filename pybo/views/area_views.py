from flask import Flask, Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect
import pandas as pd
from pybo.models import Conf_Local
from pybo import db

bp = Blueprint("area", __name__, url_prefix="/area")

def init_data():
    df = pd.read_csv("pybo\static\data\covid_data_korea_local.csv")
    
    covid_data_local = df[['gubun', 'deathCnt', 'defCnt', 'stdDay', 'incDec']].loc[(df["gubun"]!="합계")&(df["gubun"]!="검역")].drop_duplicates(subset=["gubun", "stdDay"]).reset_index().drop(columns=["index"])

    for x in covid_data_local.index:
        temp_data =Conf_Local(localName=covid_data_local.iloc[x, 0],
                              deathCnt=int(covid_data_local.iloc[x, 1]),
                              confCase=covid_data_local.iloc[x, 2],
                              createDt=covid_data_local.iloc[x, 3],
                              incDec=covid_data_local.iloc[x, 4]
                              )
        db.session.add(temp_data)
    db.session.commit()

def find_data(date):
    return Conf_Local.query.filter_by(createDt=date).all()

@bp.route("show_data", methods=["GET", "POST"])
def show_data():
    #if request.method == "GET":

    api_key = ""
    with open("pybo\static\data\\api_keys.txt", "r", encoding="utf-8") as f:
        api_key = f.readline()
        
    return render_template("area/test.html", api_key=api_key)
    #return render_template("area/showArea.html", date=request.form["date"])
    #return render_template("showArea.html", find_data())