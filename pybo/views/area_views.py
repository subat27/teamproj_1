from flask import Flask, Blueprint, render_template, g, request, url_for, current_app
from werkzeug.utils import redirect
from pybo.models import ConfLocal, ConfAge, ConfGender, Country
from pybo import db
from flask import json
from datetime import datetime
from .main_views import saveFile
from sqlalchemy import create_engine

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

import folium
import branca
import geopandas

matplotlib.use('Agg')
plt.ioff()
from .main_views import saveFile
from datetime import datetime
from sqlalchemy import create_engine


bp = Blueprint("area", __name__, url_prefix="/area")

def find_data(date):
    return ConfLocal.query.filter_by(createDt=date).order_by(ConfLocal.createDt.desc())

# 국내 현황 페이지 연결
@bp.route("/domestic",methods=("GET",))
def domestic():
    return render_template("status/domestic.html")

# 해외 현황 페이지 연결
@bp.route("/overseas",methods=("GET",))
def overseas():
    return render_template("status/overseas.html", countries=Country.query.all())


@bp.route("show_data", methods=["GET", "POST"])
def show_data():
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    data = pd.read_sql("select * from ConfLocal", engine)

    saveFile(data, "local_data")

    return render_template("area/showArea.html", datasets=find_data("2020-02-08"))


# 기능 테스트용 코드
@bp.route("/test")
def test():
    return render_template("area/test.html")

@bp.route("test2")
def test2():
    createDtList = ConfAge.getColumnList(db.session)
    print(type(createDtList))
    print(type(createDtList[0]))

    return ""

# 지역별 정보를 화면에 출력해주는 기능
@bp.route("show_geo_data", methods=["GET"])
def show_geo_data():
    return render_template("domestic/domestic_area.html")


def covid_data_by_date(df1, df2, date):
    # df1: geo_data
    dateStr = datetime.strptime(date, "%Y-%m-%d")
    filter = df2["stdDay"]==dateStr
    df2 = df2[filter] # 특정날짜 df
    df2 = df2[['gubunEn', 'deathCnt', 'defCnt', 'gubun']]
    return pd.merge(df1, df2, left_on="CTP_ENG_NM", right_on="gubunEn", how="inner").drop(columns="gubunEn")


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