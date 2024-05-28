from flask import Blueprint, render_template
import pandas as pd
from pybo.models import ConfAge, ConfGender, ConfLocal
from pybo import db

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("")
def index():
    return render_template("index.html")


# @bp.route("init")
def init_data():
    # 지역 데이터 초기화 
    covid_local = pd.read_csv("pybo\static\data\covid_data_korea_local.csv")
    covid_local = covid_local[['stdDay', 'gubun', 'gubunEn', 'defCnt', 'deathCnt']]

    covid_local = covid_local.rename(columns={'stdDay' : '기준일시',
                            'gubun': '시도명',
                            'gubunEn' : '시도명(영어)',
                            'defCnt' : '확진자수',
                            'deathCnt' : '사망자수'
                            })
    filter = (covid_local["시도명"]!="합계")&(covid_local["시도명"]!="검역")
    covid_local = covid_local.loc[filter]
    covid_local = covid_local.drop_duplicates(subset=["시도명", "기준일시"])
    covid_local = covid_local.sort_values(['기준일시', '확진자수'], ascending=[True,True])
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
                                                'confCase' : '확진자 수',
                                                'death' : '사망자',
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
                                          'confCase' : '확진자 수',
                                          'death' : '사망자'
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

    return "완료오"