from flask import Flask, Blueprint, render_template
from pybo.models import ConfLocal, ConfAge
from pybo import db
from flask import json

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

import folium

matplotlib.use('Agg')
plt.ioff()

# 국내의 코로나 데이터를 지역별로 출력하기 위해 데이터를 수정하는 코드

bp = Blueprint("area", __name__, url_prefix="/area")

def init_DB():
    # 국내 데이터 초기화
    covid_local = pd.read_csv("pybo\static\data\domestic_covid_data(local).csv")
    covid_local = covid_local[['stdDay', 'gubun', 'gubunEn', 'defCnt', 'deathCnt']]
    covid_local = covid_local.rename(columns={'stdDay' : '등록일시', 'gubun': '시도명', 'gubunEn' : '시도명(영문)', 'defCnt' : '확진자수', 'deathCnt' : '사망자수'})
    filter1 = (covid_local["시도명"]!="합계")&(covid_local["시도명"]!="검역")
    filter2 = ~((covid_local["등록일시"]>"2022-01-01")&(covid_local["확진자수"]==covid_local["사망자수"]))
    covid_local = covid_local.loc[filter1 & filter2]
    covid_local = covid_local.drop_duplicates(subset=["시도명", "등록일시"])
    covid_local = covid_local.sort_values(['등록일시', '시도명'], ascending=[True,True])
    covid_local = covid_local.reset_index().drop(columns=["index"])

    for x in covid_local.index:
        db.session.add(ConfLocal(createDt=covid_local.iloc[x, 0],
                                 localName=covid_local.iloc[x, 1],
                                 localNameEn=covid_local.iloc[x, 2],
                                 confCase=int(covid_local.iloc[x, 3]),
                                 deathCnt=int(covid_local.iloc[x, 4])))



def find_data(date):
    return ConfLocal.query.filter_by(createDt=date).order_by(ConfLocal.createDt.desc())

# 국내 현황 페이지 연결
@bp.route("/domestic", methods=["POST"])
def domestic():
    with open("pybo\static\data\domestic_geodata.json", "r", encoding="utf-8") as file:
        geo = json.loads(file.read())
        file.close()
    conf_local_list = []
    for x in ConfLocal.query.all() :
        data = {
            'createDt' : x.createDt,
            'localName' : x.localName,
            'localNameEn' : x.localNameEn,
            'confCase' : x.confCase,
            'deathCnt' : x.deathCnt
        }
        conf_local_list.append(data)

    covid_geo_df = covid_data_by_date(pd.DataFrame(conf_local_list), "2023-08-31")
    covid_geo_df = covid_geo_df.rename(columns={'createDt' : '등록일시', 'localName': '시도명', 'localNameEn' : '시도명(영문)', 'confCase' : '확진자수', 'deathCnt' : '사망자수'})

    covid_map = folium.Map(location=[36.3, 128.1], zoom_start=7, zoom_control=True, control_scale=True)

    cp = folium.Choropleth(
        geo_data=geo,
        name="choropleth",
        data=covid_geo_df,
        key_on="feature.properties.CTP_ENG_NM",
        columns=["시도명(영문)", "확진자수"],
        fill_color="Oranges"
    ).add_to(covid_map)

    state_data_indexed = covid_geo_df.set_index('시도명(영문)')
  
    for s in cp.geojson.data['features']:
        s['properties']['confCase'] = int(state_data_indexed.loc[s['properties']['CTP_ENG_NM'], "확진자수"])
  
    popup = folium.GeoJsonPopup(
        fields=['CTP_KOR_NM', "confCase"],
        aliases=["지역명", "누적확진자"],
        localize=True,
        labels=True,
        style="""
            background-color: yellow;
            border: none;
        """
    ).add_to(cp.geojson)

    folium.LayerControl().add_to(covid_map)

    return covid_map._repr_html_()


def covid_data_by_date(df, date):
    filter_date = date
    if date > df["createDt"].max():
        filter_date = df["createDt"].max()
    
    filter = df["createDt"]==filter_date

    return df[filter]