import pickle

from sklearn.ensemble import RandomForestRegressor

from random_forest.data.data_generator import DataGenerator


class Trainer(object):
    def __init__(self, target_name='price'):
        self.target_name = target_name

    def train(self):
        data_generator = DataGenerator(target_name=self.target_name, db=1)
        # 随机森林回归器
        # clf = RandomForestRegressor(n_estimators=100, random_state=0)
        clf = RandomForestRegressor(n_estimators=100, max_depth=None, min_samples_split=2)
        X, y = data_generator.generate_data()
        # 拟合数据集
        clf.fit(X, y)
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
