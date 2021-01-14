from json_handler.json_handler import load_jsonl_data
from preprocessing.junk_remover import JunkRemover


class Preprocessor:
    def __init__(self):
        self.junk_remover = JunkRemover()

    def _get_clean_data(self, input_sessions, input_users):
        return self.junk_remover.delete_junk_data(input_sessions, input_users)

    def preprocess(self, input_users, input_sessions, input_products):
        pass


class NNPreprocessor(Preprocessor):

    def preprocess(self, input_users, input_sessions, input_products):
        return self._get_clean_data(input_sessions, input_products)


def read_input_data(users_file_path="data/input/users.jsonl", sessions_file_path="data/input/sessions.jsonl",
                    products_file_path="data/input/products.jsonl"):
    input_users = load_jsonl_data(users_file_path)
    input_sessions = load_jsonl_data(sessions_file_path)
    input_products = load_jsonl_data(products_file_path)
    return input_users, input_sessions, input_products


def main():
    input_users, input_sessions, input_products = read_input_data()
    preprocessor = NNPreprocessor()
    x, y = preprocessor.preprocess(input_users, input_sessions, input_products)


if __name__ == '__main__':
    main()
