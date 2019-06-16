from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
import joblib

df = pd.read_excel('data_final.xlsx')

### knn model ###
'''根據LASSO，挑A085, A10, B03, B04, B05作為x變數'''
df_X = df[['A085', 'A10', 'B03', 'B04', 'B05']]
df_y = df[['Actual_lvl']]

X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size=0.3)

''' build the model'''
knn = KNeighborsClassifier()
knn.fit(X_train, y_train.values.ravel())

'''找合適的n'''
for i in range(1, 60):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train.values.ravel())
    pred_i = knn.predict(X_test)
    print(knn.score(X_train, y_train))

'''用模型預測並驗證準確度'''
knn.predict(X_train)
knn.score(X_train, y_train)

'''儲存模型'''
joblib.dump(knn, 'knn_model.pkl')
data = [0, 1, 4, 3, 5]
data_in = pd.DataFrame([data])
knn.predict(data_in)

