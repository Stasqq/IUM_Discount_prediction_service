import json
import os

from json_handler.json_handler import load_jsonl_data
from preprocessing.junk_remover import JunkRemover

sessions = load_jsonl_data("data/input/sessions.jsonl")
products = load_jsonl_data("data/input/products.jsonl")
jr = JunkRemover()

clean_sessions, clean_products = jr.delete_junk_data(sessions, products)

if not os.path.exists('./clean_data'):
    os.makedirs('./clean_data')

with open('./clean_data/clean_sessions.json', 'w') as session_file:
    json.dump(clean_sessions, session_file, indent=4)
with open('./clean_data/clean_products.json', 'w') as products_file:
    json.dump(clean_products, products_file, indent=4)

