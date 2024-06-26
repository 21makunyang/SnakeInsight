import pickle

import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from random_forest.data.data_generator import DataGenerator

"""
需要训练就将random_forest/__init__.py中内容注释掉
"""


class Trainer(object):
    def __init__(self, target_name='price'):
        self.target_name = target_name

    def train(self):
        data_generator = DataGenerator(target_name=self.target_name, db=1)
        # 随机森林回归器
        # clf = RandomForestRegressor(n_estimators=100, random_state=0)
        clf = RandomForestRegressor(n_estimators=100, max_depth=None, min_samples_split=2)
        X, y = data_generator.generate_data()
        print(len(X))
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # 拟合数据集
        clf.fit(X_train, y_train)
        # 使用测试集进行测试并输出结果
        y_pred = clf.predict(X_test)
        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
        print('Root Mean Squared Error:',
              np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
        print('coefficient R^2:', clf.score(X_test, y_test))

        with open(f'../ckpt/random_forest_model_{self.target_name}.pkl', 'wb') as f:
            pickle.dump(clf, f)

    def test(self):
        with open(f'../ckpt/random_forest_model_{self.target_name}.pkl', 'rb') as f:
            clf = pickle.load(f)
            # area, region, floor, has_elevator, living_room, bedroom, space
            # test_X = [['庆丰', '白云', 4, 0, 0, 1, 25.0]]
            if self.target_name == 'price':
                test_X = [[163, 5, 4, 0, 0, 1, 25.0]]
                test_y = [399]
            else:
                test_X = [[163, 5, 4, 0, 0, 1, 399]]
                test_y = [25.0]
            res = clf.predict(test_X)
            print(res)


if __name__ == '__main__':
    trainer = Trainer('price')
    trainer.train()
    trainer.test()
    trainer = Trainer('space')
    trainer.train()
    trainer.test()
