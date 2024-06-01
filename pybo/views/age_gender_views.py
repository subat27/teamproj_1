from flask import Blueprint, jsonify
import pandas as pd
from pybo.models import ConfAge, ConfGender
from pybo import db

bp = Blueprint("age_gender", __name__, url_prefix="/age_gender")

def init_DB():
    df = pd.read_csv("pybo\static\data\domestic_covid_data(age, gender).csv")
    df = df[['createDt', 'gubun', 'confCase', 'death']]
    df = df.drop_duplicates(subset=["createDt", "gubun"])

    filter = (df["gubun"]=="Male") | (df["gubun"]=="Female")

    # 성별 DataFrame -> DB 데이터
    covid_gender = df.loc[filter]
    covid_gender = covid_gender.rename(columns={'createDt' : '등록일시', 'gubun': '성별', 'confCase' : '확진자수', 'death' : '사망자수'})
    covid_gender['성별'] = covid_gender['성별'].apply(lambda x : "여성" if (x=="Female") else "남성")
    covid_gender = covid_gender.sort_values(['등록일시', '성별'], ascending=[True, True])
    covid_gender = covid_gender.reset_index().drop(columns=["index"])

    for x in covid_gender.index:
        db.session.add(ConfGender(createDt=covid_gender.iloc[x, 0],
                                  gender=covid_gender.iloc[x, 1],
                                  confCase=int(covid_gender.iloc[x, 2]),
                                  deathCnt=int(covid_gender.iloc[x, 3])))

    # 연령대 DataFrame -> DB 데이터
    covid_age = df.loc[~filter]
    covid_age = covid_age.rename(columns={'createDt' : '등록일시', 'gubun' : '연령', 'confCase' : '확진자수', 'death' : '사망자수'})

    covid_age['연령'] = covid_age['연령'] + '(세)'
    covid_age['연령'].replace({'80 over(세)':'80이상(세)'}, inplace=True)
    covid_age = covid_age.sort_values(['등록일시', '연령'], ascending=[True,True])
    covid_age = covid_age.reset_index().drop(columns=["index"])

    for x in covid_age.index:
        db.session.add(ConfAge(createDt=covid_age.iloc[x, 0],
                               ageArea=covid_age.iloc[x, 1],
                               confCase=int(covid_age.iloc[x, 2]),
                               deathCnt=int(covid_age.iloc[x, 3])))

# 연령대별 코로나 확진자 정보를 가져오는 함수
@bp.route("/get_age_data", methods=["post"])
def get_age_data():
    conf_age_list = ConfAge.query.all()    
    datasets = {}
    for x in conf_age_list:
        data = {
            'createDt' : x.createDt,
            'confCase' : x.confCase,
            'deathCnt' : x.deathCnt
        }
        temp = datasets.get(x.ageArea, list())
        temp.append(data)
        datasets.setdefault(x.ageArea, temp)

    return jsonify(datasets)

# 성별 코로나 확진자 정보를 가져오는 함수
@bp.route("/get_gender_data", methods=["post"])
def get_gender_data():
    conf_gender_list = ConfGender.query.all()
    datasets = {}
    for x in conf_gender_list:
        data = {
            'createDt' : x.createDt,
            'confCase' : x.confCase,
            'deathCnt' : x.deathCnt
        }
        temp = datasets.get(x.gender, list())
        temp.append(data)
        datasets.setdefault(x.gender, temp)

    return jsonify(datasets)