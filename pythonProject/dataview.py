import pandas as pd


def get_formatted_data(data: dict) -> str:
    return str(pd.DataFrame(data)) if data else 'Пусто'
