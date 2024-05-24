from flask import Flask, Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect
#import pandas as pd
from pybo.models import ConfLocal
from pybo import db
import os
from flask import json

bp = Blueprint("area", __name__, url_prefix="/area")

def init_data():
    df = pd.read_csv("pybo\static\data\covid_data_korea_local.csv")
    
    covid_data_local = df[['gubun', 'deathCnt', 'defCnt', 'stdDay', 'incDec', 'gubunEn']].loc[(df["gubun"]!="합계")&(df["gubun"]!="검역")].drop_duplicates(subset=["gubun", "stdDay"]).reset_index().drop(columns=["index"])

    for x in covid_data_local.index:
        temp_data =ConfLocal(localName=covid_data_local.iloc[x, 0],
                              deathCnt=int(covid_data_local.iloc[x, 1]),
                              confCase=covid_data_local.iloc[x, 2],
                              createDt=covid_data_local.iloc[x, 3],
                              incDec=covid_data_local.iloc[x, 4],
                              localNameEn=covid_data_local.iloc[x, 5]
                              )
        db.session.add(temp_data)
    db.session.commit()

# 뭘하는 함수인 지 ex 
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



