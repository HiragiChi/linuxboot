#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from random import seed
from random import randrange
from math import sqrt
from math import exp
from math import pi
from sklearn.feature_selection import mutual_info_classif
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier  
import operator
import plotly.express as px
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from sklearn import tree
import graphviz
import matplotlib.pyplot as plt
from numpy import mean, std


# In[2]:


from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix


# In[3]:


from sklearn.metrics import precision_recall_fscore_support as score


# In[4]:


from sklearn.metrics import classification_report


# In[5]:


from xgboost import XGBClassifier


# In[55]:


from sklearn.neural_network import MLPClassifier


# In[57]:


from sklearn.externals import joblib


# In[56]:


import pickle


# In[7]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[8]:


import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


# In[9]:


malware_db = mysql.connector.connect(host='localhost', database='ELF', user='ELF', password='toor')


# In[10]:


mal_cursor = malware_db.cursor()


# In[11]:


sql = "SELECT `peframe_ip`, `peframe_url`, `readelf_entry_address`, `readelf_start_prog_headers`, `readelf_start_sec_headers`, `readelf_number_flags`, `readelf_header_size`, `readelf_size_prog_headers`, `readelf_number_prog_headers`, `readelf_size_sec_headers`, `readelf_number_section_headers`,`readelf_sec_header_string_table_index`, `strings_number`, `strings_size`, `strings_avg`, `file_size`, `file_entropy` FROM `processed` where `type` in ('DDos', 'Trojan', 'Backdoor', 'Virus', 'Exploit', 'DoS', 'PUA', 'TrojanDownloader', 'Worm', 'VirTool' );"


# In[12]:


test_sql = "SELECT `peframe_ip`, `peframe_url`, `readelf_entry_address`, `readelf_start_prog_headers`, `readelf_start_sec_headers`, `readelf_number_flags`, `readelf_header_size`, `readelf_size_prog_headers`, `readelf_number_prog_headers`, `readelf_size_sec_headers`, `readelf_number_section_headers`,`readelf_sec_header_string_table_index`, `strings_number`, `strings_size`, `strings_avg`, `file_size`, `file_entropy` FROM `processed` where `type` not in ('DDos', 'Trojan', 'Backdoor', 'Virus', 'Exploit', 'DoS', 'PUA', 'TrojanDownloader', 'Worm', 'VirTool' );"


# In[13]:


mal_cursor.execute(sql)
mal_result = mal_cursor.fetchall()


# In[14]:


mal_cursor.execute(test_sql)
mal_test_result = mal_cursor.fetchall()


# In[15]:


mal_cursor.close()
malware_db.close()


# In[16]:


len(mal_result)


# In[17]:


len(mal_test_result)


# |字段名称|值|
# |---|---|
# |`peframe_ip`|0|
# |`peframe_url`|0|
# |`readelf_entry_address`|0x8048c20(134515744)|
# |`readelf_start_prog_headers`|52|
# |`readelf_start_sec_headers`|60616|
# |`readelf_number_flags`|1|
# |`readelf_header_size`|52|
# |`readelf_size_prog_headers`|32|
# |`readelf_number_prog_headers`|6|
# |`readelf_size_sec_headers`|40|
# |`readelf_number_section_headers`|29|
# |`readelf_sec_header_string_table_index`|26|
# |`strings_number`|832|
# |`strings_size`|27121|
# |`strings_avg`|32.5947|
# |`file_entropy`|5.88998|

# In[70]:


vnames = ['peip', 'peurl', 'ep', 'sph', 'ssh', 'nf', 'hs', 'szph', 'nph', 'szsh', 'nsh', 'shsti', 'sn', 'ss', 'sa', 'fe']


# In[38]:


benign_db = mysql.connector.connect(host='localhost', database='ELF_benign_new', user='ELF', password='toor')
benign_cursor = benign_db.cursor()
ben_sql = "SELECT `peframe_ip`, `peframe_url`, `readelf_entry_address`, `readelf_start_prog_headers`, `readelf_start_sec_headers`, `readelf_number_flags`, `readelf_header_size`, `readelf_size_prog_headers`, `readelf_number_prog_headers`, `readelf_size_sec_headers`, `readelf_number_section_headers`,`readelf_sec_header_string_table_index`, `strings_number`, `strings_size`, `strings_avg`, `file_size`, `file_entropy` FROM `processed`;"
benign_cursor.execute(ben_sql)
ben_result = benign_cursor.fetchall()
benign_cursor.close()
benign_db.close()


# In[39]:


benign_x32_db = mysql.connector.connect(host='localhost', database='ELF_benign_x32', user='ELF', password='toor')
benign_x32_cursor = benign_x32_db.cursor()
ben_x32_sql = "SELECT `peframe_ip`, `peframe_url`, `readelf_entry_address`, `readelf_start_prog_headers`, `readelf_start_sec_headers`, `readelf_number_flags`, `readelf_header_size`, `readelf_size_prog_headers`, `readelf_number_prog_headers`, `readelf_size_sec_headers`, `readelf_number_section_headers`,`readelf_sec_header_string_table_index`, `strings_number`, `strings_size`, `strings_avg`, `file_size`, `file_entropy` FROM `processed`;"
benign_x32_cursor.execute(ben_x32_sql)
ben_x32_result = benign_x32_cursor.fetchall()
benign_x32_cursor.close()
benign_x32_db.close()


# In[40]:


len(ben_result)


# In[41]:


len(ben_x32_result)


# In[42]:


ben_X = np.concatenate((np.array(ben_result), np.array(ben_x32_result)), axis=0)
mal_X = np.array(mal_result)
mal_test_X = np.array(mal_test_result)


# In[43]:


len(mal_X)


# In[53]:


mal_X[0].shape


# In[44]:


len(mal_test_X)


# In[45]:


mal_y = np.array([1 for i in range(len(mal_X))])
ben_y = np.array([0 for i in range(len(ben_X))])
mal_test_y = np.array([1 for i in range(len(mal_test_X))])


# In[46]:


# data
X = np.concatenate((mal_X, ben_X), axis=0)
y = np.concatenate((mal_y, ben_y), axis=0)
# Z可以进行调整，删除某一行
# Z = np.concatenate((X[:,:2], X[:,3:]), axis=1)


# In[47]:


XY = list(zip(X, y))
random.seed(1234)
random.shuffle(XY)

X, y = zip(*XY)


# In[48]:


rate = 0.8
split = int(len(X) * rate)


# In[49]:


X = np.array(X)
y = np.array(y)


# In[50]:


target_names = ["benign", "malware"]


# In[67]:


# model = RandomForestClassifier()
# model = DecisionTreeClassifier()
# model = AdaBoostClassifier()
# model = KNeighborsClassifier()
model = XGBClassifier()
# model = MLPClassifier()
# print(len(X[:split]))
model.fit(X[:split,2:], y[:split])
# print(model.score(X[:split], y[:split]))
y_pred = model.predict(X[split:,2:])
print(classification_report(y[split:], y_pred, target_names=target_names, digits=4))
# precision, recall, fscore, support = score(y[split:], y_pred)

# print('precision: {}'.format(precision))
# print('recall: {}'.format(recall))
# print('fscore: {}'.format(fscore))
# print('support: {}'.format(support))
# print(f1_score(y[split:], y_pred, average="macro"))
# print(precision_score(y[split:], y_pred, average="macro"))
# print(recall_score(y[split:], y_pred, average="macro"))    
# print(model.score(X[split:], y[split:]))
print("------------")
test_y_pred = model.predict(mal_test_X[:,2:])
# print(classification_report(mal_test_y, test_y_pred, target_names=target_names, digits=4))
# print(len(test_y_pred))
precision, recall, fscore, support = score(mal_test_y, test_y_pred)
print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('fscore: {}'.format(fscore))
print('support: {}'.format(support))
# print(f1_score(mal_test_y, test_y_pred, average="macro"))
# print(precision_score(mal_test_y, test_y_pred, average="macro"))
# print(recall_score(mal_test_y, test_y_pred, average="macro"))   
# print(model.score(mal_test_X, mal_test_y))
# cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
# n_scores = cross_val_score(model, X, y, scoring='accuracy', cv=cv, n_jobs=-1, error_score='raise')
# print('准确率: %.3f (%.3f)' % (mean(n_scores), std(n_scores)))
joblib.dump(model, "xgboost.pkl")


# In[71]:


res = dict(zip(vnames,
               mutual_info_classif(X, y, discrete_features=True)
               ))
print(res)


# In[69]:


X[1]


# In[72]:


dict(sorted(res.items(), key=lambda item: item[1], reverse=True))


# |字段名称|值|
# |---|---|
# |`peframe_ip`|0|
# |`peframe_url`|0|
# |`readelf_entry_address`|0x8048c20(134515744)|
# |`readelf_start_prog_headers`|52|
# |`readelf_start_sec_headers`|60616|
# |`readelf_number_flags`|1|
# |`readelf_header_size`|52|
# |`readelf_size_prog_headers`|32|
# |`readelf_number_prog_headers`|6|
# |`readelf_size_sec_headers`|40|
# |`readelf_number_section_headers`|29|
# |`readelf_sec_header_string_table_index`|26|
# |`strings_number`|832|
# |`strings_size`|27121|
# |`strings_avg`|32.5947|
# |`file_entropy`|5.88998|

# In[28]:


import seaborn as sns


# In[29]:


X_ep = np.array(X)[:,2]
X_fe = np.array(X)[:,15]
X_sa = np.array(X)[:,14]
X_nph = np.array(X)[:,8]


# In[30]:


XY_ep = list(zip(X_ep, y))
XY_fe = list(zip(X_fe, y))
XY_sa = list(zip(X_sa, y))
XY_nph = list(zip(X_nph, y))


# In[31]:


cnt = 0
for item in XY_fe:
    if item[1] == 0:
        cnt += 1
print(cnt)


# In[32]:


sub_df = pd.DataFrame(data=XY_fe, columns=['entropy', '属性'] )


# In[48]:


sns.axes_style()


# In[69]:



# myfont = FontProperties(fname=r'/usr/share/fonts/chinese/simsun.ttc',size=14)
# sns.boxplot(data=np.array(XY_fe), whis=np.inf, color='indianred')
# plt.rcParams['font.sans-serif'] = ['SimSun']
# plt.rcParams['axes.unicode_minus'] = False 
# sns.set_context("talk")
# sns.set_style("ticks")
# sns.set_context("poster")
# sns.set(font_scale=100) 
# sns.set(font='SimHei')
# plt.rcParams.update({'font.size': 30})
sns.set_context("paper", rc={"font.size":20,"axes.titlesize":20,"axes.labelsize":20})  
plt.figure(figsize=(15, 10))
b = sns.violinplot(x="属性", y="entropy", data=sub_df)
b.set_yticklabels(b.get_yticks(), size = 15)
b.set_xticklabels(b.get_xticks(), size = 15)
plt.show()
# with sns.axes_style("dark"):
#     sns.jointplot('index', 'label', data=sub_df, kind="hist")
#     plt.ylim([-1, 2])
#     plt.xlim([0, 10])

