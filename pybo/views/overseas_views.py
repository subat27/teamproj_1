from flask import Blueprint, render_template, request
from pybo.models import Country
from pybo import db
import pandas as pd

bp = Blueprint("overseas", __name__, url_prefix="/overseas")

@bp.route("/graph")
def overseas_graph():
    country = Country.query.all()
    return render_template("overseas/overseas_graph.html", country=country)

# @bp.route("/korea")
# def korea():
#     return render_template("overseas/korea.html")

# 여기서부터 수정할 것
@bp.route("/korea", methods=('Get', 'Post'))
def korea():
    if request.method == 'GET':
        country =  Country.query.all()
        return render_template("overseas/country/korea.html", country=country)

    return render_template("overseas/country/korea.html")

@bp.route("/japan")
def japan():
    return render_template("overseas/country/japan.html")
@bp.route("/china")
def china():
    return render_template("overseas/country/china.html")
@bp.route("/russia")
def russia():
    return render_template("overseas/country/russia.html")
@bp.route("/canada")
def canada():
    return render_template("overseas/country/canada.html")
@bp.route("/usa")
def usa():
    return render_template("overseas/country/usa.html")
@bp.route("/australia")
def australia():
    return render_template("overseas/country/australia.html")
@bp.route("/brazil")
def brazil():
    return render_template("overseas/country/brazil.html")
@bp.route("/saudiarabia")
def saudiarabia():
    return render_template("overseas/country/saudiarabia.html")
@bp.route("/argentina")
def argentina():
    return render_template("overseas/country/argentina.html")
@bp.route("/unitedkingdom")
def unitedkingdom():
    return render_template("overseas/country/unitedkingdom.html")
@bp.route("/congo")
def congo():
    return render_template("overseas/country/congo.html")


# 여기까지
# 국가를 입력하면 화면에 그 국가에 대한 정보가 나타나게 구현

@bp.route("/input2", methods=('Get', 'Post'))
def db_input2():

    if request.method == 'GET':
        return render_template("overseas/country_input2.html")

    df = pd.read_csv("pybo\static\data\COVID19-global.csv")

    df1 = df.copy()
    df1 = df1.drop(columns=df1.columns[[1, 3, 5, 6, 7]])
    df1.rename(columns={'Date_reported':'날짜',
                        'Country':'국가',
                        'New_cases':'감염자'}, inplace=True)
    df1["날짜"] = pd.to_datetime(df1["날짜"])
    
    # 240국가를 db에 저장해주는 코드 ######
    for name in df1["국가"].unique():
        print(":::::::::::::::::::")
        print(name)
        country = Country(name=name)
        db.session.add(country)
        db.session.commit()

    return render_template("")
 