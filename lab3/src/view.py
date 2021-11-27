import pandas as pd


def get_formatted_data(data: dict) -> str:
    dict_rec = [vars(a) for a in data]
    [a.pop('_sa_instance_state', None) for a in dict_rec]
    return str(pd.DataFrame(dict_rec)) if dict_rec else 'Нічого не знайдено!'
