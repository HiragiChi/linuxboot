#%% 
import joblib
import numpy as np
import os
from get_one_elf_features import get_one_elf_features 
import sys

# model = joblib.load(filename="decisiontreemdl.pkl")
# model = joblib.load(filename="adaboostmdl.pkl")     
# model = joblib.load(filename="knnmdl.pkl")          
# model = joblib.load(filename="./models/randomforestmdl.pkl")
model = joblib.load(filename="xgboostmdl.pkl")

elf_file= sys.argv[1]
X_test=np.zeros(shape=(0,15))

f = open(elf_file)
file_test = f.readlines()
for file in file_test:
    feature=get_one_elf_features(file[:-1])
    X_test=np.append(X_test,feature)

f.close()
# print(X_test.shape)
X_test=X_test.reshape(-1,15)

Result=model.predict(X_test)
# print(Result)
# print(Result.shape)

index=np.nonzero(Result)
# print(index)

mare_filelist = [file_test[int(i)] for i in index[0]]
f = open("Marefile","w")
f.writelines(mare_filelist)
f.close()
# print(mare_filelist)

nums=len(file_test)
mare_nums=len(mare_filelist)
print(nums,mare_nums,'%.2f%%' %((1-mare_nums/nums)*100))
# %%
