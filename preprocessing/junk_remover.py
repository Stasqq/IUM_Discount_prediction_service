from preprocessing.session_user_filler import SessionUserFiller
from preprocessing.timestamp_handler import TimestampHandler


class FunkRemover:

    def __init__(self):
        self._session_user_filler = SessionUserFiller()
        self._timestamp_handler = TimestampHandler()

    def delete_junk_data(self, sessions, products):
        new_sessions = self._clear_sessions(sessions)

    def _clear_sessions(self, sessions):
        sessions = self._session_user_filler.fill_sessions_users(sessions)
        sessions = self._delete_sessions_without(sessions, 'user_id')
        sessions = self._delete_sessions_without(sessions, 'product_id')
        sessions = self._drop_buy_sessions_without_purchase_id(sessions)
        sessions = self._timestamp_handler.turn_timestamp_into_age(sessions)
        return sessions

    def _delete_sessions_without(self, sessions, attribute):
        return [session for session in sessions if session[attribute] is not None]

    def _drop_buy_sessions_without_purchase_id(self, sessions):
        return [session for session in sessions if not
        (session['event_type'] == 'BUY_PRODUCT' and session['purchase_id'] is None)]
