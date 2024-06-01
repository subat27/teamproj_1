from flask import Blueprint, render_template, redirect
from pybo import db
from pybo.views import age_gender_views, area_views, overseas_views

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("")
def index():
    return render_template("index.html")

@bp.route("initDB")
def init_DB():
    age_gender_views.init_DB()  # 성별 / 연령별 데이터 초기화
    area_views.init_DB()        # 국내 지역 데이터 초기화     
    overseas_views.init_DB()    # 해외 지역 데이터 초기화
        
    db.session.commit()

    return redirect("/")

@bp.route("domestic")
def domestic():
    return render_template("status/domestic.html")


@bp.route("overseas")
def overseas():
    return render_template("status/overseas.html")