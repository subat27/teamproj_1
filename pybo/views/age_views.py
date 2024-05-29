from flask import Flask, Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect
import os
from datetime import datetime

bp = Blueprint("age", __name__, url_prefix="/age")

@bp.route("show/<nation>")
def show(nation):
    # filter = df["국가명"]==nation
    # df[filter].plot().save_fig()  데이터프레임을 html/png 파일로 저장
    return render_template("")


def saveFile(df, area):
    filename = area
    upload_path = makedirectory()
    path = os.path.join(upload_path, filename)
    path = path.replace("\\", "/")

    df.loc[df["지역명"]==area].save(path)

    idx = path.find("/static/charts")

    return path[idx:]

def makedirectory():
    UPLOAD_DIR="pybo/static/charts"
    name_ymd = datetime.now().strftime("%Y%m%d")

    new_dir_path = os.path.join(UPLOAD_DIR, name_ymd)

    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    return new_dir_path
