import pickle

with open(f'../random_forest/ckpt/random_forest_model_space.pkl', 'rb') as f:
    space_random_forest = pickle.load(f)

with open(f'../random_forest/ckpt/random_forest_model_price.pkl', 'rb') as f:
    price_random_forest = pickle.load(f)