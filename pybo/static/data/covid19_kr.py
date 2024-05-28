#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pandas')
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['font.size'] = 15
mpl.rcParams['axes.unicode_minus'] = False


# In[2]:


df1 = pd.read_csv("covid_data_korea.csv")
df1


# In[3]:


filter1 = df1["gubun"]=="Male"
filter2 = df1["gubun"]=="Female"


# In[4]:


covid_gender = df1.loc[filter1 | filter2]
covid_gender


# In[5]:


covid_gender = covid_gender.rename(columns={'criticalRate': '치명률',
                                       'death' : '사망자',
                                       'deathRate' : '사망률',
                                       'confCaseRate' : '확진율',
                                       'createDt' : '등록일시',
                                       'confCase' : '확진자 수',
                                       'gubun': '성별'})              
covid_gender


# In[10]:


covid_gender = covid_gender.sort_values(['등록일시'], ascending=[True])
covid_gender


# In[11]:


covid_gender['등록일시'] = pd.to_datetime(covid_gender['등록일시'])


# In[12]:


filter11 = covid_gender["등록일시"].dt.month==6
filter22 = covid_gender["등록일시"].dt.year==2022
filter44 = covid_gender["등록일시"].dt.day==15

filter55 = filter11 & filter22 & filter44
covid_gender_filter = covid_gender[filter55]


# In[14]:


covid_gender_filter.set_index(covid_gender_filter['성별'], inplace=True)

ratio = covid_gender_filter["확진자 수"]
labels = covid_gender_filter.index

plt.pie(ratio, labels=labels, autopct='%.1f%%')
plt.title("성별 확진율")
plt.show()


# In[15]:


covid_age = df1.loc[~filter1 & ~filter2]
covid_age


# In[16]:


covid_age = covid_age.rename(columns={'criticalRate': '치명률',
                                       'death' : '사망자',
                                       'deathRate' : '사망률',
                                       'confCaseRate' : '확진율',
                                       'createDt' : '등록일시',
                                       'confCase' : '확진자 수',
                                       'gubun' : '연령'})              
covid_age


# In[17]:


covid_age['연령'] = covid_age['연령'] + '(세)'
covid_age


# In[18]:


covid_age['연령'].replace({'80 over(세)':'80이상(세)'}, inplace=True)
covid_age


# In[20]:


covid_age = covid_age.sort_values(['등록일시', '연령'], ascending=[True,True])
covid_age


# In[21]:


covid_age['등록일시'] = pd.to_datetime(covid_age['등록일시'])


# In[22]:


filter11=covid_age["연령"]=="0-9(세)"
covid_age_09 = covid_age[filter11]
covid_age_09


# In[23]:


filter11=covid_age["연령"]=="10-19(세)"
covid_age_19 = covid_age[filter11]
covid_age_19


# In[24]:


filter11=covid_age["연령"]=="20-29(세)"
covid_age_29 = covid_age[filter11]
covid_age_29


# In[25]:


filter11=covid_age["연령"]=="30-39(세)"
covid_age_39 = covid_age[filter11]
covid_age_39


# In[26]:


filter11=covid_age["연령"]=="40-49(세)"
covid_age_49 = covid_age[filter11]
covid_age_49


# In[27]:


filter11=covid_age["연령"]=="50-59(세)"
covid_age_59 = covid_age[filter11]
covid_age_59


# In[28]:


filter11=covid_age["연령"]=="60-69(세)"
covid_age_69 = covid_age[filter11]
covid_age_69


# In[29]:


filter11=covid_age["연령"]=="70-79(세)"
covid_age_79 = covid_age[filter11]
covid_age_79


# In[30]:


filter11=covid_age["연령"]=="80이상(세)"
covid_age_89 = covid_age[filter11]
covid_age_89


# In[31]:


fig, ax = plt.subplots(figsize=(8,6))
sns.lineplot(data=covid_age_09, x='등록일시', y='확진자 수', ax=ax)
sns.lineplot(data=covid_age_19, x='등록일시', y='확진자 수', ax=ax)
sns.lineplot(data=covid_age_29, x='등록일시', y='확진자 수', ax=ax)
sns.lineplot(data=covid_age_39, x='등록일시', y='확진자 수', ax=ax)
sns.lineplot(data=covid_age_49, x='등록일시', y='확진자 수', ax=ax)
sns.lineplot(data=covid_age_59, x='등록일시', y='확진자 수', ax=ax)
sns.lineplot(data=covid_age_69, x='등록일시', y='확진자 수', ax=ax)
sns.lineplot(data=covid_age_79, x='등록일시', y='확진자 수', ax=ax)
sns.lineplot(data=covid_age_89, x='등록일시', y='확진자 수', ax=ax)
plt.xticks(rotation=45) 
plt.yticks(np.arange(2100000, 2500000, step=500000))
plt.gca().get_yaxis().set_major_formatter(StrMethodFormatter('{x:,.0f}'))


# In[33]:


filter1 = covid_age["등록일시"].dt.month==6
filter2 = covid_age["등록일시"].dt.year==2022
filter4 = covid_age["등록일시"].dt.day==15

filter5 = filter1 & filter2 & filter4
covid_age_filter = covid_age[filter5]


# In[34]:


covid_age_filter.set_index(covid_age_filter['연령'], inplace=True)

ratio = covid_age_filter["확진자 수"]
labels = covid_age_filter.index

plt.pie(ratio, labels=labels, autopct='%.1f%%')
plt.title("연령별 확진율")
plt.show()


# In[35]:


covid_local = pd.read_csv("covid_data_korea_local.csv")
covid_local


# In[36]:


covid_local = covid_local.rename(columns={'gubunEn' : '시도명(영어)',
                          'deathCnt' : '사망자수',
                          'defCnt' : '확진자수',
                          'isolClearCnt' : '격리해제수',
                          'stdDay' : '기준일시',
                          'localOccCnt' : '지역발생수',
                          'qurRate' : '10만명당발생률',
                          'overFlowCnt' : '해외유입수',
                          'gubunCn' : '시도명(중국)',
                          'incDec' : '전일대비증감수',
                          'isolIngCnt' : '격리중환자수',
                          'gubun': '시도명'})       
covid_local


# In[37]:


covid_local = covid_local.sort_values(['기준일시', '지역발생수'], ascending=[True,True])
covid_local


# In[38]:


covid_local = covid_local.drop(columns=['시도명(영어)', '사망자수', '확진자수', '격리해제수', '해외유입수', '시도명(중국)', '전일대비증감수', '격리중환자수'])
covid_local


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




