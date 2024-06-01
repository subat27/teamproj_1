from flask import Blueprint, request, jsonify
from werkzeug.utils import redirect
from pybo.models import ConfGlobal
from pybo import db
import pandas as pd
from datetime import datetime
import folium

bp = Blueprint("overseas", __name__, url_prefix="/overseas")

# 해외의 코로나 데이터를 출력하기 위해 데이터를 수정하는 코드

def init_DB():
    df1 = pd.read_csv("pybo\static\data\overseas_covid_data.csv")
    df2 = pd.read_csv("pybo\static\data\country_code.csv")

    df1[["New_deaths", "New_cases"]] = df1[["New_deaths", "New_cases"]].fillna(0).copy()
    df1.drop(columns=["WHO_region"], inplace=True)

    covid_global = pd.merge(df1, df2, how="inner", left_on="Country_code", right_on="code")
    covid_global = covid_global[['Date_reported', 'name(kr)', 'name(en)', 'Cumulative_cases', 'Cumulative_deaths', 'New_cases', 'New_deaths', 'code']]
    covid_global["code"] = covid_global["code"].fillna("NB")

    covid_global = covid_global.rename(columns={'Date_reported' : '등록일시', 'name(kr)': '국가명', 'name(en)' : '국가명(영문)', 'Cumulative_cases' : '확진자수',
                                                'Cumulative_deaths' : '사망자수', 'New_cases' : '신규확진자수', 'New_deaths' : '신규사망자수', 'code' : '국가코드'})

    for x in covid_global.index:
        db.session.add(ConfGlobal(createDt=covid_global.iloc[x, 0],
                                  nation_kr=covid_global.iloc[x, 1],
                                  nation_en=covid_global.iloc[x, 2],
                                  confCase=int(covid_global.iloc[x, 3]),
                                  deathCnt=int(covid_global.iloc[x, 4]),
                                  newConfCase=int(covid_global.iloc[x, 5]),
                                  newDeathCase=int(covid_global.iloc[x, 6]),
                                  code=covid_global.iloc[x, 7]))

@bp.route("getCountryList", methods=["POST"])
def getCountryList():
    conf_global_list = ConfGlobal.query.all()

    country_list = {}

    for x in conf_global_list:
        country_list.setdefault(x.nation_kr, x.code)

    return jsonify(country_list)

@bp.route("getData", methods=["POST"])
def getData():
    data = request.json
    code = data.get("code")
    
    conf_global_list = ConfGlobal.query.filter_by(code=code).all()

    datasets = {}

    for x in conf_global_list:
        data = {
            "createDt" : x.createDt,
            "confCase" : x.confCase,
            "deathCnt" : x.deathCnt,
            "newConfCase" : x.newConfCase,
            "newDeathCase" : x.newDeathCase,
        }
        temp = datasets.get(x.nation_kr, list())
        temp.append(data)
        datasets.setdefault(x.nation_kr, temp)

    return jsonify(datasets)

# 전세계 정보를 화면에 출력해주는 기능
@bp.route("get_html", methods=["POST"])
def create_global_geo_data():
    with open("pybo\static\data\overseas_geodata.geojson", "r", encoding="utf-8") as file:
        geo = file.read()
        file.close()

    conf_global_list = []
    for x in ConfGlobal.query.filter_by(createDt="2024-05-12").all():
        data = {
            "nation_kr" : x.nation_kr,
            "nation_en" : x.nation_en,
            "confCase" : x.confCase,
            "deathCnt" : x.deathCnt,
            "newConfCase" : x.newConfCase,
            "newDeathCase" : x.newDeathCase,
            "code" : x.code
        }
        conf_global_list.append(data)

    
    covid_global_geo_df = pd.DataFrame(conf_global_list)
    covid_global_geo_df = covid_global_geo_df.rename(columns={"nation_kr" : "국가명", "nation_en" : "국가명(영문)", "confCase" : "누적확진자수", "deathCnt" : "누적사망자수", "newConfCase" : "신규확진자수", "newDeathCase" : "신규사망자수", "code" : "국가코드"})

    covid_map = folium.Map(location=[51.95, 19.15], zoom_start=2, zoom_control=True, control_scale=True)

    cp = folium.Choropleth(
        geo_data=geo,
        name="choropleth",
        data=covid_global_geo_df,
        key_on="feature.properties.ISO",
        columns=["국가코드", "누적확진자수"],
        fill_color="Blues",
        fill_opacity=0.8,
        line_opacity=0.8,
        
    ).add_to(covid_map)

    state_data_indexed = covid_global_geo_df.set_index('국가코드')
    for s in cp.geojson.data['features']:
        try:
            s['properties']['confCase'] = int(state_data_indexed.loc[s['properties']['ISO'], "누적확진자수"])
            s['properties']['COUNTRY_KR'] = state_data_indexed.loc[s['properties']['ISO'], "국가명"]
        except:
            pass
    
    popup = folium.GeoJsonPopup(
        fields=["COUNTRY_KR", "confCase"],
        aliases=["국가명", "누적확진자"],
        localize=True,
        labels=True,
        style="""
            background-color: yellow;
            border: none;
        """
    ).add_to(cp.geojson)

    folium.LayerControl().add_to(covid_map)

    return covid_map._repr_html_()
