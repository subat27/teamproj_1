from flask import Flask, Blueprint, render_template, g, request, url_for
from werkzeug.utils import redirect
import os
from datetime import datetime
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pybo.models import ConfGender
from pybo import db

bp = Blueprint("gender", __name__, url_prefix="/gender")

# 국내의 코로나 데이터를 성별로 출력하기 위해 데이터를 수정하는 코드

@bp.route("/create_gender_chart_img")
def init_global_data():
    
    print(type(ConfGender.getColumnList(db.session)))
    print(ConfGender.getColumnList(db.session)[0])
    

    return ""
    # for area in df1["국가"].unique():
    #     saveFile(df1, area)

    # return redirect("")


# def saveFile(df, area):
#     filename = area + ".png"
#     upload_path = makedirectory()
#     path = os.path.join(upload_path, filename)
#     path = path.replace("\\", "/")

#     filter=df["국가"]==area 
#     temp_df = df[filter]
#     temp_df.plot(x="날짜", y=["신규확진자"])
#     plt.savefig(path)

#     idx = path.find("/static/img")

#     return path[idx:]

# def makedirectory():
#     UPLOAD_DIR="pybo/static/img"
#     name_ymd = datetime.now().strftime("%Y%m%d")

#     new_dir_path = os.path.join(UPLOAD_DIR, name_ymd)

#     if not os.path.exists(new_dir_path):
#         os.mkdir(new_dir_path)

#     return new_dir_path

