
class DeckAttrs:
    COLORS = ('r', 'g', 'b', 'y')
    DRAWS = (1, 2, 4)
    ACTIONS = ('s', 'r', '+2')
    DRAWS_TYPE_VALUES = {
        '+2': 2,
        '+4': 4,
    }
    INITIAL_DEAL_COUNT = 7

    @staticmethod
    def get_base_deck():
        """Returns a tuple of all the cards expected in a basic deck."""
        base_deck = []
        base_deck.extend(('w',) * 4)
        base_deck.extend(('w+4',) * 4)
        for color in DeckAttrs.COLORS:
            for n in range(10):
                base_deck.extend((f'{color}{n}',) * 2)
            for action in DeckAttrs.ACTIONS:
                base_deck.extend((f'{color}{action}',) * 2)
        return tuple(base_deck)
