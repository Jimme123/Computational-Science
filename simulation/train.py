class Train(PositionalAgent):
    def __init__(self, model, position, speed):
        super().__init__(model, position)
        self.speed = speed

    def move(self, direction):
        next_position = self.position + self.speed * direction

        signal = self.model.rails.next_signal(next_position)

        if signal == "RED":
            self.speed = 0
        else:
            self.position = next_position

    def step(self):
        self.move(direction = 1)
