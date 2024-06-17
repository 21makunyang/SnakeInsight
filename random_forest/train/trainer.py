from sklearn.ensemble import RandomForestRegressor

from random_forest.data.data_generator import DataGenerator

data_generator = DataGenerator(db=1)
# 随机森林回归器
clf = RandomForestRegressor(n_estimators=100, random_state=0)
X, y = data_generator.generate_data()
# 拟合数据集
clf = clf.fit(X, y)

# area, region, floor, has_elevator, living_room, bedroom, space
# test_X = [['庆丰', '白云', 4, 0, 0, 1, 25.0]]
test_X = [[163, 32, 4, 0, 0, 1, 25.0]]
test_y = [399]
res = clf.predict(test_X)
print(res)
