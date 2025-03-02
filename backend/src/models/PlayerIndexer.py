
class PlayerIndexer:
    """Manages the index of the current player."""

    def __init__(self):
        self._increment = 1
        self._index = 0
        # The number of players
        self._count = 1
        self._skip = False

    def increment_handler(self):
        """Increment the index of the current player."""
        # Guard against skipping a player
        if self._skip:
            self._skip = False
            return

        self._index += self._increment

    def reverse(self):
        """Reverse the increment direction, or skip the other player when there are only 2 players."""
        if self._count == 2:
            # Reverse cards function as skip cards when there are only 2 players.
            self._skip = True
            return
        self._increment = -self._increment

    def add_player(self):
        self._count += 1

    def remove_player(self):
        self._count -= 1

    @property
    def count(self):
        return self._count

    @property
    def index(self):
        return self._index
