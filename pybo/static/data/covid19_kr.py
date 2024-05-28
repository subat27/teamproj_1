
# import pandas as pd
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
# from datetime import datetime
# from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
# mpl.rcParams['font.family'] = 'Malgun Gothic'
# mpl.rcParams['font.size'] = 15
# mpl.rcParams['axes.unicode_minus'] = False


# # 성별 / 연령별 데이터
# df1 = pd.read_csv("covid_data_korea.csv")

# # 성별 데이터
# filter = (df1["gubun"]=="Male") & (df1["gubun"]=="Female")
# covid_gender = df1.loc[filter]
# covid_gender = covid_gender.rename(columns={'criticalRate': '치명률',
#                                        'death' : '사망자',
#                                        'deathRate' : '사망률',
#                                        'confCaseRate' : '확진율',
#                                        'createDt' : '등록일시',
#                                        'confCase' : '확진자 수',
#                                        'gubun': '성별'})

# covid_gender = covid_gender.sort_values(['등록일시', '성별'], ascending=[True])
# covid_gender = covid_gender.reset_index()
# covid_gender = covid_gender.drop(columns=["index"])
# covid_gender['등록일시'] = pd.to_datetime(covid_gender['등록일시'])


# # 연령대별 데이터

# covid_age = df1.loc[~filter]
# covid_age = covid_age.rename(columns={'criticalRate': '치명률',
#                                        'death' : '사망자',
#                                        'deathRate' : '사망률',
#                                        'confCaseRate' : '확진율',
#                                        'createDt' : '등록일시',
#                                        'confCase' : '확진자 수',
#                                        'gubun' : '연령'})              

# covid_age['연령'] = covid_age['연령'] + '(세)'
# covid_age['연령'].replace({'80 over(세)':'80이상(세)'}, inplace=True)
# covid_age = covid_age.sort_values(['등록일시', '연령'], ascending=[True,True])
# covid_age = covid_age.reset_index()
# covid_age = covid_age.drop(columns=["index"])
# covid_age['등록일시'] = pd.to_datetime(covid_age['등록일시'])






# # test
# fig, ax = plt.subplots(figsize=(8,6))

# for x in covid_age["연령"].unique():
#     filter1 = covid_age["연령"]==x
#     covid_age_temp = covid_age[filter1]
#     sns.lineplot(data=covid_age_temp, x='등록일시', y='확진자 수', ax=ax)
    
# plt.xticks(rotation=45) 
# plt.yticks(np.arange(2100000, 2500000, step=500000))
# plt.gca().get_yaxis().set_major_formatter(StrMethodFormatter('{x:,.0f}'))

# plt.xticks(rotation=45) 
# plt.yticks(np.arange(2100000, 2500000, step=500000))
# plt.gca().get_yaxis().set_major_formatter(StrMethodFormatter('{x:,.0f}'))


# # 특정 날짜 데이터 test pie foam
# filter11 = covid_gender["등록일시"].dt.month==6
# filter22 = covid_gender["등록일시"].dt.year==2022
# filter44 = covid_gender["등록일시"].dt.day==15
# filter55 = filter11 & filter22 & filter44
# covid_gender_filter = covid_gender[filter55]
# covid_gender_filter.set_index(covid_gender_filter['성별'], inplace=True)
# ratio = covid_gender_filter["확진자 수"]
# labels = covid_gender_filter.index
# plt.pie(ratio, labels=labels, autopct='%.1f%%')
# plt.title("성별 확진율")
# plt.show()

# filter1 = covid_age["등록일시"].dt.month==6
# filter2 = covid_age["등록일시"].dt.year==2022
# filter4 = covid_age["등록일시"].dt.day==15
# filter5 = filter1 & filter2 & filter4
# covid_age_filter = covid_age[filter5]
# covid_age_filter.set_index(covid_age_filter['연령'], inplace=True)
# ratio = covid_age_filter["확진자 수"]
# labels = covid_age_filter.index
# plt.pie(ratio, labels=labels, autopct='%.1f%%')
# plt.title("연령별 확진율")
# plt.show()





# ###################################################################################################################

# covid_local = pd.read_csv("pybo\static\data\covid_data_korea_local.csv")
# covid_local = covid_local[['gubun', 'deathCnt', 'defCnt', 'stdDay', 'gubunEn']]

# covid_local = covid_local.rename(columns={'gubunEn' : '시도명(영어)',
#                           'deathCnt' : '사망자수',
#                           'defCnt' : '확진자수',
#                           'stdDay' : '기준일시',
#                           'gubun': '시도명'})
# filter = (covid_local["시도명"]!="합계")&(covid_local["시도명"]!="검역")
# covid_local = covid_local.loc[filter]
# covid_local = covid_local.drop_duplicates(subset=["시도명", "기준일시"])
# covid_local = covid_local.sort_values(['기준일시', '지역발생수'], ascending=[True,True])
# covid_local = covid_local.reset_index()
# covid_local = covid_local.drop(columns=["index"])

# for x in covid_data_local.index:
#         temp_data =ConfLocal(localName=covid_data_local.iloc[x, 0],
#                               deathCnt=int(covid_data_local.iloc[x, 1]),
#                               confCase=covid_data_local.iloc[x, 2],
#                               createDt=covid_data_local.iloc[x, 3],
#                               incDec=covid_data_local.iloc[x, 4],
#                               localNameEn=covid_data_local.iloc[x, 5]
#                               )
#         db.session.add(temp_data)
#     db.session.commit()
    

