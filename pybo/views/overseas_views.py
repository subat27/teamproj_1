from flask import Blueprint, render_template, send_file
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from io import BytesIO

bp = Blueprint("overseas", __name__, url_prefix="/overseas")

df = pd.read_csv("pybo/static/data/covid19 age-sex.csv")

df1 = df.copy()
df1=df1.drop(columns=df1.columns[3:5])

df1.rename(columns={'country':'국가',
                    'date':'날짜',
                    'age_group':'나이대',
                    'casesF':'여성 감염',
                    'casesM':'남성 감염',
                    'populationin1000sF':'여성 인구',
                    'populationin1000sM':'남성 인구'
                   }, inplace=True)

df1 = df1.drop(columns=df1.columns[5:])
df1["날짜"] = pd.to_datetime(df1["날짜"])

filter1=df1["날짜"].dt.month==6 
filter2=df1["날짜"].dt.year==2022    

filter3 = filter1 & filter2
df2=df1[filter3]


filter11=df2["국가"]=="Japan" # 일본이라는 국가명을 찾는 필터
df21 = df2[filter11]
filter12=df2["국가"]=="USA" # 미국
df22 = df2[filter12]  
filter13=df2["국가"]=="England" # 영국
df23 = df2[filter13]
filter14=df2["국가"]=="Canada" # 캐나다
df24 = df2[filter14]
filter15=df2["국가"]=="Australia" # 오스트레일리아
df25 = df2[filter15]
filter16=df2["국가"]=="Germany"   # 독일
df26 = df2[filter16]
filter17=df2["국가"]=="Israel"  # 이스라엘
df27= df2[filter17]
filter18=df2["국가"]=="Italy"  # 이탈리아
df28 = df2[filter18]
filter19=df2["국가"]=="Mexico" # 멕시코
df29 = df2[filter19]
filter20=df2["국가"]=="Netherlands" # 네덜란드
df30 = df2[filter20]
filter21=df2["국가"]=="Spain" # 스페인
df31= df2[filter21]
filter22=df2["국가"]=="Taiwan" # 대만
df32 = df2[filter22]

df21.set_index(df21['나이대'], inplace=True) #일본, 인덱스를 '나이대'로 변경
df22.set_index(df22['나이대'], inplace=True) #미국 
df23.set_index(df23['나이대'], inplace=True) #영국 
df24.set_index(df24['나이대'], inplace=True) #캐나다 
df25.set_index(df25['나이대'], inplace=True) #오스트레일리아 
df26.set_index(df26['나이대'], inplace=True) #독일 
df27.set_index(df27['나이대'], inplace=True) #이스라엘
df28.set_index(df28['나이대'], inplace=True) #이탈리아 
df29.set_index(df29['나이대'], inplace=True) #멕시코 
df30.set_index(df30['나이대'], inplace=True) #네덜란드 
df31.set_index(df31['나이대'], inplace=True) #스페일 
df32.set_index(df32['나이대'], inplace=True) #대만


@bp.route("/bar")
def bar():

    df21.plot(kind="bar", x="나이대", y=["여성 감염", "남성 감염"])
    
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    return send_file(img, mimetype='image/png')




@bp.route("/graph")
def overseas_graph():

    return render_template("overseas/overseas_graph.html")