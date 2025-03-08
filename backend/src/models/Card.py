from models.DeckAttrs import DeckAttrs


class Card:
    def __init__(self, value: str):
        self.value = value
        self.wild = False
        self.color = None
        self.number = None
        self.draw_count = 0
        self.reverse = False
        self.skip = False
        self.action = None
        if value.endswith('+4'):
            self.draw_count = 4
        elif value.endswith('+2'):
            self.draw_count = 2
        elif value.endswith('r'):
            self.reverse = True
        elif value.endswith('s'):
            self.skip = True
        # Wild cards and draw four wild cards
        if value.startswith('w'):
            self.wild = True

        if not self.wild:
            color = value[0]
            if color not in DeckAttrs.COLORS:
                raise ValueError(f'Invalid color: {color}')
            self.color = color

        remainder = value[1:]
        if not remainder:
            # No remainder means card represents a chosen color
            return

        if remainder.isdigit():
            self.number = int(remainder)
            if self.number < 0 or self.number > 9:
                raise ValueError(f'Invalid card value: {value}')
        elif remainder in DeckAttrs.ACTIONS + ('+4',):
            self.action = remainder
        else:
            raise ValueError(f'Invalid card value: {value}')

    def is_playable(self, current_card: 'Card'):
        """Check if the card is playable on the current card."""
        return (
            self.wild or
            self.color == current_card.color or
            self.number == current_card.number
        )

    def __repr__(self):
        return f'Card(color={self.color}, number={self.number}, wild={self.wild}, draw_count={self.draw_count})'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value
