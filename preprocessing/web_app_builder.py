import pickle
from array import array
from datetime import datetime
import pandas as pd

from json_handler.json_handler import load_json_data, load_jsonl_data


def get_user_id_from_user(user):
    return int(user.partition(":")[0])


def get_product_id_from_product(product):
    return int(product.partition(":")[0])


class ModelPrediction:
    def __init__(self, prediction):
        self.prediction = prediction


class WebAppPredictionHolder:
    def __init__(self):
        self.first_model = ModelPrediction([])
        self.second_model = ModelPrediction([])


class Product:
    def __init__(self, product_id, price, category):
        self.product_id = product_id
        self.price = price
        self.category = category


class User:
    def __init__(self):
        self.products_views_number = dict()
        self.category_views_number = dict()
        self.bought_with_discount_number = dict()
        self.bought_products_in_category_number = dict()


class Session:
    def __init__(self, user, product, timestamp, event_type, discount, session_id):
        self.user = user
        self.product = product
        self.timestamp = timestamp
        self.event_type = event_type
        self.discount = discount
        self.session_id = session_id


class Record:
    def __init__(self, price, products_views_number, category_views_number, bought_with_discount_number,
                 bought_products_in_category_number, discount, elapsed_time):
        self.price = price
        self.products_views_number = products_views_number
        self.category_views_number = category_views_number
        self.bought_with_discount_number = bought_with_discount_number
        self.bought_products_in_category_number = bought_products_in_category_number
        self.discount = discount
        self.elapsed_time = elapsed_time


class WebAppBuilder:
    def __init__(self):
        self._clean_products = load_json_data('clean_data/clean_products.json')
        self._clean_users = load_jsonl_data('data/input/users.jsonl')
        self._create_users_sessions_dict()
        self.prediction_holder = WebAppPredictionHolder()
        with open('models/dummy.pckl', 'rb') as file:
            self.dummy = pickle.load(file)
        with open('models/regression.pckl', 'rb') as file:
            self.regression = pickle.load(file)

    def get_products_for_web(self):
        return [f'{product["product_id"]}:{product["product_name"]}:{product["price"]}' for product in
                self._clean_products]

    def get_users_for_web(self):
        return [f'{user["user_id"]}:{user["name"]}' for user in self._clean_users]

    def _create_users_sessions_dict(self):
        sessions_list = load_jsonl_data('prepared_data/prepared_sessions.jsonl')
        products_list = load_json_data('prepared_data/preapred_products.json')
        users_list = load_jsonl_data('data/input/users.jsonl')

        self.products = dict()
        for product in products_list:
            self.products[product['product_id']] = Product(product['product_id'], product['price'],
                                                           product['category_path'])

        self.users = dict()
        for user in users_list:
            self.users[user['user_id']] = User()

        sessions = list()
        for session in sessions_list:
            user = self.users[session['user_id']]
            product = self.products[session['product_id']]
            sessions.append(Session(user, product, session['timestamp'], session['event_type'],
                                    session['offered_discount'], session['session_id']))

        records = list()
        current_session_id = 0
        last_session_timestamp = 0
        elapsed_time = 0
        for session in sessions:
            if current_session_id != session.session_id:
                current_session_id = session.session_id
                last_session_timestamp = session.timestamp
                elapsed_time = datetime.strptime(last_session_timestamp, '%Y-%m-%dT%H:%M:%S') - datetime.strptime(
                    last_session_timestamp, '%Y-%m-%dT%H:%M:%S')
            else:
                elapsed_time = datetime.strptime(session.timestamp, '%Y-%m-%dT%H:%M:%S') - datetime.strptime(
                    last_session_timestamp, '%Y-%m-%dT%H:%M:%S')
                last_session_timestamp = session.timestamp

            elapsed_time = elapsed_time.total_seconds()

            price = session.product.price

            products_views_number = session.user.products_views_number.get(session.product.product_id, 0)
            session.user.products_views_number[session.product.product_id] = products_views_number + 1

            category_views_number = session.user.category_views_number.get(session.product.category, 0)
            session.user.category_views_number[session.product.category] = category_views_number + 1

            purchases_with_discount_counter = 0
            for x in range(0, session.discount + 1, 5):
                purchases_with_discount_counter += session.user.bought_with_discount_number.get(x, 0)

            purchases_in_category_number = \
                session.user.bought_products_in_category_number.get(session.product.category, 0)

            if session.event_type == 0:
                session.user.bought_with_discount_number[session.discount] = \
                    session.user.bought_with_discount_number.get(session.discount, 0) + 1
                session.user.bought_products_in_category_number[session.product.category] = \
                    purchases_in_category_number + 1

    def _get_merged_session_data(self, user_id, product_id, discount):
        user = self.users[user_id]
        product = self.products[product_id]
        serializable_dict = dict()

        serializable_dict['price'] = [product.price]

        serializable_dict['product_views_number'] = [user.products_views_number.get(product.product_id, 0)]
        #user.products_views_number[product.product_id] = serializable_dict['product_views_number'] + 1

        serializable_dict['category_views_number'] = [user.category_views_number.get(product.category, 0)]
        #user.category_views_number[product.category] = serializable_dict['category_views_number'] + 1

        serializable_dict['bought_with_discount_number'] = [user.bought_with_discount_number.get(discount, 0)]

        serializable_dict['bought_products_in_category_number'] = [user.bought_products_in_category_number.get(
            product.category, 0)]
        #user.bought_products_in_category_number[product.category] = serializable_dict[
                                      #                                  'bought_products_in_category_number'] + 1

        # tu przy predykcji trzeba wstawiac w petli kolejne wartosci discount
        serializable_dict['discount'] = [discount]

        # todo:: ile tu wstawiac
        serializable_dict['elapsed_time'] = [100]

        serializable_dict['oh_category0'] = [1] if product.category == 'Gry i konsole;Gry komputerowe' else [0]
        serializable_dict[
            'oh_category1'] = [1] if product.category == 'Gry i konsole;Gry na konsole;Gry PlayStation3' else [0]
        serializable_dict['oh_category2'] = [1] if product.category == 'Gry i konsole;Gry na konsole;Gry Xbox 360' else [0]
        serializable_dict[
            'oh_category3'] = [1] if product.category == 'Komputery;Drukarki i skanery;Biurowe urządzenia wielofunkcyjne' else [0]
        serializable_dict['oh_category4'] = [1] if product.category == 'Komputery;Monitory;Monitory LCD' else [0]
        serializable_dict['oh_category5'] = [1] if product.category == 'Komputery;Tablety i akcesoria;Tablety' else [0]
        serializable_dict['oh_category6'] = [1] if product.category == 'Sprzęt RTV;Audio;Słuchawki' else [0]
        serializable_dict[
            'oh_category7'] = [1] if product.category == 'Sprzęt RTV;Przenośne audio i video;Odtwarzacze mp3 i mp4' else [0]
        serializable_dict['oh_category8'] = [1] if product.category == 'Sprzęt RTV;Video;Odtwarzacze DVD' else [0]
        serializable_dict[
            'oh_category9'] = [1] if product.category == 'Sprzęt RTV;Video;Telewizory i akcesoria;Anteny RTV' else [0]
        serializable_dict[
            'oh_category10'] = [1] if product.category == 'Sprzęt RTV;Video;Telewizory i akcesoria;Okulary 3D' else [0]
        serializable_dict[
            'oh_category11'] = [1] if product.category == 'Telefony i akcesoria;Akcesoria telefoniczne;Zestawy głośnomówiące' else [0]
        serializable_dict[
            'oh_category12'] = [1] if product.category == 'Telefony i akcesoria;Akcesoria telefoniczne;Zestawy słuchawkowe' else [0]
        serializable_dict['oh_category13'] = [1] if product.category == 'Telefony i akcesoria;Telefony komórkowe' else [0]
        serializable_dict['oh_category14'] = [1] if product.category == 'Telefony i akcesoria;Telefony stacjonarne' else [0]
        return serializable_dict

    def predict_with_first_model(self, user, product):
        loop_counter = 1
        user_id = get_user_id_from_user(user)
        product_id = get_product_id_from_product(product)
        for discount in range(0, 21, 5):
            model_input_data = self._get_merged_session_data(user_id, product_id, discount)
            #prediction = self.dummy.predict(pd.DataFrame(model_input_data))
            #print(loop_counter)
            #print(prediction)
            score = self.dummy.score(pd.DataFrame(model_input_data), [1])
            print(score)
            if score > 0.8:
                self.prediction_holder.first_model.prediction = [user, product, discount]
                return
            loop_counter += 1
        self.prediction_holder.first_model.prediction = [user, product, 'nie kupi']

    def predict_with_second_model(self, user, product):
        user_id = get_user_id_from_user(user)
        product_id = get_product_id_from_product(product)
        loop_counter = 1
        for discount in range(0, 21, 5):
            model_input_data = self._get_merged_session_data(user_id, product_id, discount)
            #prediction = self.regression.predict(pd.DataFrame(model_input_data))
            #print(loop_counter)
            #print(prediction)
            score = self.regression.score(pd.DataFrame(model_input_data), [1])
            print(score)
            if score > 0.8:
                self.prediction_holder.second_model.prediction = [user, product, discount]
                return
            loop_counter += 1
        self.prediction_holder.second_model.prediction = [user, product, 'nie kupi']
