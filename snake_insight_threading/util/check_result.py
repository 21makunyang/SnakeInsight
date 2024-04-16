import pickle


def get_result(file_path: str):
    with open(f'{file_path}', 'br') as pkl:
        obj = pickle.load(pkl)

    print(obj)


if __name__ == '__main__':
    get_result(r'E:\Projects\SnakeInsight\snake_insight\tmp\city_house_info_1712925854.pkl')
