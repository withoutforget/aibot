from dataclasses import dataclass

TelegramID = int


@dataclass()
class UserData:
    username: str
    tokens_used: int = 0
    promts_generated: int = 0


class UserResoucres:
    _data: dict[TelegramID, UserData] = dict()

    def user_exist(self, id: TelegramID) -> bool:
        return id in self._data.keys()

    def add_user(self, id: TelegramID, username: str) -> bool:
        if self.user_exist(id):
            return False
        self._data[id] = UserData(username)
        return True

    def increment_tokens(self, id: TelegramID, tokens: int) -> bool:
        if not self.user_exist(id):
            return False
        self._data[id].tokens_used += tokens
        self._data[id].promts_generated += 1
        return True
