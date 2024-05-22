from flask import Flask, Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect
import pandas as pd
from pybo.models import Conf_Local
from pybo import db

bp = Blueprint("area", __name__, url_prefix="/area")

@bp.route("init_data")
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

    return render_template("area/showArea.html")

@bp.route("find_data")
def find_data():
    covid_datas = Conf_Local.query.filter_by(createDt='2022-01-28').all()
    print(covid_datas[0].confCase)
    print(covid_datas[0].incDec)
    print(covid_datas[0].deathCnt)


    df = pd.read_csv("pybo\static\data\covid_data_korea_local.csv")
    
    covid_data_local = df[['gubun', 'deathCnt', 'defCnt', 'stdDay', 'incDec']].loc[(df["gubun"]!="합계")&(df["gubun"]!="검역")].drop_duplicates(subset=["gubun", "stdDay"]).reset_index().drop(columns=["index"])


    print(type(covid_data_local.iloc[0, 0]))
    print(type(covid_data_local.iloc[0, 1]))
    print(type(covid_data_local.iloc[0, 2]))
    print(type(covid_data_local.iloc[0, 3]))
    print(type(covid_data_local.iloc[0, 4]))
    



    return render_template("area/resultTest.html", covid_datas=covid_datas)