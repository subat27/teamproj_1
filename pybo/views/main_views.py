from flask import Blueprint, render_template, redirect
import pandas as pd
from pybo.models import ConfAge, ConfGender, ConfLocal
from pybo import db
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import mpld3
from datetime import datetime
mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['font.size'] = 15
mpl.rcParams['axes.unicode_minus'] = False
mpl.use('Agg')
plt.ioff()


bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("")
def index():
    return render_template("index.html")

@bp.route("initDB")
def init_data():
    # 지역 데이터 초기화 
    covid_local = pd.read_csv("pybo\static\data\covid_data_korea_local.csv")
    covid_local = covid_local[['stdDay', 'gubun', 'gubunEn', 'defCnt', 'deathCnt']]

    covid_local = covid_local.rename(columns={'stdDay' : '등록일시',
                            'gubun': '시도명',
                            'gubunEn' : '시도명(영어)',
                            'defCnt' : '확진자수',
                            'deathCnt' : '사망자수'
                            })
    filter = (covid_local["시도명"]!="합계")&(covid_local["시도명"]!="검역")&~((covid_local["등록일시"]>"2022-01-01")&(covid_local["확진자수"]==covid_local["사망자수"]))
    covid_local = covid_local.loc[filter]
    covid_local = covid_local.drop_duplicates(subset=["시도명", "등록일시"])
    covid_local = covid_local.sort_values(['등록일시', '시도명'], ascending=[True,True])
    covid_local = covid_local.reset_index()
    covid_local = covid_local.drop(columns=["index"])

    for x in covid_local.index:
        temp_data =ConfLocal(createDt=covid_local.iloc[x, 0],
                             localName=covid_local.iloc[x, 1],
                             localNameEn=covid_local.iloc[x, 2],
                             confCase=covid_local.iloc[x, 3],
                             deathCnt=int(covid_local.iloc[x, 4]),
                            )
        db.session.add(temp_data)


    # 성별 / 연령별 데이터 초기화 
    df1 = pd.read_csv("pybo\static\data\covid_data_korea.csv")
    df1 = df1[['createDt', 'gubun', 'confCase', 'death']]
    df1 = df1.drop_duplicates(subset=["createDt", "gubun"])
    
    # 성별 데이터
    filter = (df1["gubun"]=="Male") | (df1["gubun"]=="Female")
    covid_gender = df1.loc[filter]
    covid_gender = covid_gender.rename(columns={'createDt' : '등록일시',
                                                'gubun': '성별',
                                                'confCase' : '확진자수',
                                                'death' : '사망자수',
                                                })
    covid_gender = covid_gender.sort_values(['등록일시', '성별'], ascending=[True, True])
    covid_gender = covid_gender.reset_index()
    covid_gender = covid_gender.drop(columns=["index"])

    for x in covid_gender.index:
        temp_data =ConfGender(createDt=covid_gender.iloc[x, 0],
                              gender=covid_gender.iloc[x, 1],
                              confCase=covid_gender.iloc[x, 2],
                              deathCnt=covid_gender.iloc[x, 3]
                              )
        db.session.add(temp_data)


    # 연령대별 데이터
    covid_age = df1.loc[~filter]
    covid_age = covid_age.rename(columns={'createDt' : '등록일시',
                                          'gubun' : '연령',
                                          'confCase' : '확진자수',
                                          'death' : '사망자수'
                                          })

    covid_age['연령'] = covid_age['연령'] + '(세)'
    covid_age['연령'].replace({'80 over(세)':'80이상(세)'}, inplace=True)
    covid_age = covid_age.sort_values(['등록일시', '연령'], ascending=[True,True])
    covid_age = covid_age.reset_index()
    covid_age = covid_age.drop(columns=["index"])

    for x in covid_age.index:
        temp_data =ConfAge(createDt=covid_age.iloc[x, 0],
                              ageArea=covid_age.iloc[x, 1],
                              confCase=covid_age.iloc[x, 2],
                              deathCnt=covid_age.iloc[x, 3]
                              )
        db.session.add(temp_data)
    
    db.session.commit()

    return redirect("/")


def saveFile(df, area):
    # jpg 파일로 저장
    filename = area + ".jpg"
    upload_path = makedirectory()

    path = os.path.join(upload_path, filename)
    path = path.replace("\\", "/")
    df['createDt'] = pd.to_datetime(df['createDt'])
    if not checkFile(path):
        fig = plt.figure(figsize=(13, 8), layout='constrained')
        for localName in df["localName"].unique():
            temp_df = df[df["localName"]==localName]
            plt.plot(temp_df['createDt'], temp_df['confCase'], label=localName)
            plt.xlabel('등록일시')
            plt.ylabel('확진자수')
            plt.legend()
        plt.savefig(path)
        plt.close()

    idx = path.find("/static/charts")

    return path[idx:]

def makedirectory():
    UPLOAD_DIR="pybo/static/charts"
    name_ymd = datetime.now().strftime("%Y%m%d")

    new_dir_path = os.path.join(UPLOAD_DIR, name_ymd)

    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    return new_dir_path

def checkFile(path):
    if os.path.exists(path):
        return True

    return False
