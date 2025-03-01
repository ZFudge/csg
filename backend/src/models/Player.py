from models import Hand


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = Hand()

    def get_name(self):
        return self.name
