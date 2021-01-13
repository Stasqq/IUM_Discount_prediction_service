from json_handler.json_handler import load_json_data, load_jsonl_data


def get_user_id_from_user(user):
    return int(user.partition(":")[0])


class ModelPrediction:
    def __init__(self, prediction):
        self.prediction = prediction


class WebAppPredictionHolder:
    def __init__(self):
        self.first_model = ModelPrediction([])
        self.second_model = ModelPrediction([])


class WebAppBuilder:
    def __init__(self):
        self._clean_products = load_json_data('clean_data/clean_products.json')
        self._clean_users = load_jsonl_data('data/input/users.jsonl')

    def get_products_for_web(self):
        return [f'{product["product_name"]}:{product["category_path"]}' for product in self._clean_products]

    def get_users_for_web(self):
        return [f'{user["user_id"]}:{user["name"]}' for user in self._clean_users]
