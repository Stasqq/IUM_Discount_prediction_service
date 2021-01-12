from json_handler.json_handler import load_jsonl_data
from preprocessing.junk_remover import JunkRemover

sessions = load_jsonl_data("data/input/sessions.jsonl")
products = load_jsonl_data("data/input/products.jsonl")
jr = JunkRemover()

clean_sessions, clean_products = jr.delete_junk_data(sessions, products)

for i in range(0, len(clean_products)):
    print(clean_products[i])

