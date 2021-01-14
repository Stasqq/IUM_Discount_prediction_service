class SessionUserFiller:

    def fill_sessions_users(self, sessions):
        for index, session in enumerate(sessions):
            if session['user_id'] is None:
                session['user_id'] = self._get_user_id_from_sessions(sessions, index)
        return sessions

    def _get_user_id_from_sessions(self, sessions, index):
        prev_user_id, prev_session_id = self._prev_not_null_user_and_session_id(sessions, index)

        # w poprzednich sesjach byl ten sam numer sesji z nie null uzytkownikiem
        if prev_session_id == sessions[index]['session_id']:
            return prev_user_id

        next_user_id, next_session_id = self._next_not_null_user_and_session_id(sessions, index)

        # w kolejnych sesjach byl ten sam numer sesji z nie null uzytkownikiem
        if next_session_id == sessions[index]['session_id']:
            return next_user_id



    def _prev_not_null_user_and_session_id(self, sessions, index):
        for i in range(index, -1, -1):
            if sessions[i]['user_id'] is not None:
                return sessions[i]['user_id'], sessions[i]['session_id']

    def _next_not_null_user_and_session_id(self, sessions, index):
        for i in range(index, len(sessions)):
            if sessions[i]['user_id'] is not None:
                return sessions[i]['user_id'], sessions[i]['session_id']
