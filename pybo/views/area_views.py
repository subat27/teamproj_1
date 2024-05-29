from flask import Flask, Blueprint, render_template, g, request, url_for, current_app
from werkzeug.utils import redirect
from pybo.models import ConfLocal, ConfAge, ConfGender
from pybo import db
from flask import json
from datetime import datetime
from .main_views import saveFile
from sqlalchemy import create_engine

import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
import mpld3

import folium
import branca
import geopandas

matplotlib.use('Agg')
plt.ioff()
from .main_views import saveFile
from datetime import datetime
from sqlalchemy import create_engine



bp = Blueprint("area", __name__, url_prefix="/area")

# 뭘하는 함수인 지 ex 
def find_data(date):
    #ConfLocal.query.order_by(ConfLocal.createDt.desc())
    return ConfLocal.query.filter_by(createDt=date).order_by(ConfLocal.createDt.desc())


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
                   
                   #나라 변수 설정 아직 적용안됨
@bp.route("/search/<country_id>",methods=("POST",))
def search(country_id):
    search = request.form["search"]
    country=db.query.get(country_id)
    
                                                #글자를 하나씩나눌수있음
    return render_template("overseas/canada.html", search=search, country=country )
#=========================안영호추가




@bp.route("show_data", methods=["GET", "POST"])
def show_data():
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    data = pd.read_sql("select * from ConfLocal", engine)

    saveFile(data, "local_data")

    return render_template("area/showArea.html", datasets=find_data("2020-02-08"))


def covid_data_by_date(df1, df2, date):
    dateStr = datetime.strptime(date, "%Y-%m-%d")
    filter = df2["stdDay"]==dateStr
    df2 = df2[filter]
    df2 = df2[['gubunEn', 'deathCnt', 'defCnt', 'gubun']]
    return pd.merge(df1, df2, left_on="CTP_ENG_NM", right_on="gubunEn", how="inner").drop(columns="gubunEn")

@bp.route("show_geo_data", methods=["GET"])
def show_geo_data():
    return render_template("domestic/domestic_area.html")

@bp.route("create_geo_data", methods=["GET"])
def create_geo_data():
    with open("pybo\static\data\sido_korea.geojson", "r", encoding="utf-8") as file:
        geo = file.read()
        file.close()
        covid_df_2 = pd.read_csv("pybo\static\data\covid_data_korea_local.csv")
        korea_sido_center = pd.read_csv("pybo\static\data\sido_korea.csv")

    temp = geopandas.GeoDataFrame.from_features(json.loads(geo), crs="OGC:CRS84")
    covid_df_2["stdDay"] = pd.to_datetime(covid_df_2["stdDay"])
    temp2 = covid_data_by_date(temp, covid_df_2, "2021-05-30")

    colormap = branca.colormap.LinearColormap(
        vmin=temp2["defCnt"].quantile(0.0),
        vmax=temp2["defCnt"].quantile(1),
        colors=["darkgreen", "green", "lightblue", "orange", "red"],
        caption="확진자수"
    )

    covid_map = folium.Map(location=[36.3, 128.1], zoom_start=7, zoom_control=True, control_scale=True)

    popup = folium.GeoJsonPopup(
        fields=["gubun", "defCnt"],
        aliases=["지역명", "누적확진자"],
        localize=True,
        labels=True,
        style="""
            background-color: yellow;
            border: none;
        """
    )

    g = folium.GeoJson(
        temp2,
        style_function=lambda x : {
            "fillColor" : colormap(x["properties"]["defCnt"])
            if x["properties"]["defCnt"] is not None
            else "transparent",
            "color": "black",
            "fillOpacity": 0.5,
        },
        popup=popup,
        # tooltip=tooltip
    ).add_to(covid_map)

    colormap.add_to(covid_map)

    covid_map.save("pybo/static/data/map.html")

    return redirect("/")

@bp.route("test2")
def test2():
    createDtList = ConfAge.getColumnList(db.session)
    print(type(createDtList))
    print(createDtList[0])
    print(createDtList[3])
    print(type(createDtList[0]['ageArea']))
    print(type(createDtList[0]['confCase']))
    print(type(createDtList[0]['createDt']))
    print(type(createDtList[0]['deathCnt']))

    return render_template("area/test2.html", data=createDtList)