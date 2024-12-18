import json
import os

def get_dollar_prediction():
    """
    Retrieves dollar prediction data from 'dollar_prediction.json'.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'dollar_prediction.json')

        with open(json_path, 'r') as f:
            data = json.load(f)
            return data['fair_price']
    except FileNotFoundError:
        return {"error": "notfound"}

dataNeeded = get_dollar_prediction()

