
class PlayerIndexer:
    """Manages the index of the current player."""

    def __init__(self):
        self.step = 1
        self.index = 0
        # The number of players
        self.count = 1
        self.skip = False

    def increment(self):
        """Increment the index of the current player."""
        # Guard against skipping a player
        if self.skip:
            self.skip = False
            return

        self.index += self.step
        if self.index >= self.count:
            self.index = 0
        elif self.index < 0:
            self.index = self.count - 1

    def reverse(self):
        """Reverse the increment direction, or skip the other player when there are only 2 players."""
        if self.count == 2:
            # Reverse cards function as skip cards when there are only 2 players.
            self.skip_player()
            return
        self.step = -self.step

    def add_player(self):
        self.count += 1

    def remove_player(self):
        if self.count == 1:
            raise ValueError("Cannot remove the last player")
        self.count -= 1

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._step = value

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def skip(self):
        return self._skip

    @skip.setter
    def skip(self, value):
        self._skip = value

    def skip_player(self):
        self.skip = True
