from sklearn.ensemble import RandomForestRegressor

from random_forest.data.data_generator import DataGenerator

data_generator = DataGenerator()
# 随机森林回归器
clf = RandomForestRegressor(n_estimators=100, random_state=0)
X, y = data_generator.generate_data()
# 拟合数据集
clf = clf.fit(X, y)
