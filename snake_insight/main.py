import pickle
import time

from snake_insight.core import get_rent_info

if __name__ == '__main__':
    city_name_list = ['gz', 'sz', 'sh', 'bj']
    city_house_info = get_rent_info(city_name_list=city_name_list, page_limit=1)
    with open(f'./tmp/city_house_info_{int(time.time())}.pkl', 'bw+') as pkl:
        pickle.dump(city_house_info, pkl)
