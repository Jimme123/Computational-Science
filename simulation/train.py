from positionalAgent import *
from block import *
from block import Color

dt = 1  # tijdstap

class Train(PositionalAgent):
    def __init__(self, model, position, rails, max_speed):
        super().__init__(model, position)
        self.max_speed = max_speed
        self.speed = max_speed
        self.rails = rails
        self.rails.add_train(self)

    def move(self, direction=1):
        """
        Beweeg trein afhankelijk van het sein van het volgende blok:
        - Rood: stop
        - Oranje: halve snelheid
        - Groen: volle snelheid
        """
        # Zoek het blok waar de trein zich bevindt
        blocks_occupied = self.rails.blocks_occupied_train(self)
        next_block = None
        if blocks_occupied:
            last_block = blocks_occupied[-1]
            next_block = self.rails.get_next_block(last_block)

        # Pas snelheid aan op basis van sein
        if next_block:
            if next_block.signal == Color.RED:
                self.speed = 0
            elif next_block.signal == Color.ORANGE:
                self.speed = max(self.speed / 2, 1)
            else:
                self.speed = min(self.max_speed, self.speed*2)
        else:
            self.speed = min(self.max_speed, self.speed*2)

        # Beweeg trein langs de rail
        self.position.start += direction * self.speed * dt
        self.position.end += direction * self.speed * dt

        # Rondrijden: als einde rail bereikt, start opnieuw
        if self.position.start >= self.rails.length:
            delta = self.position.end - self.position.start
            self.position.start = 0
            self.position.end = self.position.start + delta

    def step(self):
        self.move()
