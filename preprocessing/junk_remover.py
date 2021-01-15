from preprocessing.session_user_filler import SessionUserFiller

MIN_PRODUCT_PRICE = 1
MAX_PRODUCT_PRICE = 10000

class JunkRemover:

    def __init__(self):
        self._session_user_filler = SessionUserFiller()

    def delete_junk_data(self, sessions, products):
        pre_sessions = self._clear_sessions(sessions)
        new_products = self._clear_products(products)
        new_sessions = self._remove_sessions_with_removed_products(pre_sessions, new_products)
        return new_sessions, new_products

    def _clear_sessions(self, sessions):
        sessions = self._session_user_filler.fill_sessions_users(sessions)
        sessions = self._delete_sessions_without(sessions, 'user_id')
        sessions = self._delete_sessions_without(sessions, 'product_id')
        sessions = self._drop_buy_sessions_without_purchase_id(sessions)
        return sessions

    def _delete_sessions_without(self, sessions, attribute):
        return [session for session in sessions if session[attribute] is not None]

    def _drop_buy_sessions_without_purchase_id(self, sessions):
        return [session for session in sessions if not
        (session['event_type'] == 'BUY_PRODUCT' and session['purchase_id'] is None)]

    def _clear_products(self, products):
        return [product for product in products if MIN_PRODUCT_PRICE <= product['price'] <= MAX_PRODUCT_PRICE]

    def _remove_sessions_with_removed_products(self, pre_sessions, new_products):
        new_product_ids = set()
        for product in new_products:
            new_product_ids.add(product['product_id'])
        return [session for session in pre_sessions if session['product_id'] in new_product_ids]