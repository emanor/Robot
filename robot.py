class Robot:
    DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]
    def __init__(self, x=0, y=0, energy=100, game=None): # Added game argument
        self.x = x
        self.y = y
        self.energy = energy
        self.direction = "EAST" # Default direction
        self.game = game # Store game reference for potential future use (e.g. board dimensions)

    def move_forward(self, distance):
        # Energy is consumed regardless of whether the move is valid (boundary checks in Game)
        self.energy -= distance
        if self.energy < 0:
            self.energy = 0

        if self.direction == "NORTH":
            self.y += distance
        elif self.direction == "SOUTH":
            self.y -= distance
        elif self.direction == "EAST":
            self.x += distance
        elif self.direction == "WEST":
            self.x -= distance

    def turn_left(self):
        self.energy -= 1
        if self.energy < 0:
            self.energy = 0
        current_index = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(current_index - 1) % len(self.DIRECTIONS)]

    def turn_right(self):
        self.energy -= 1
        if self.energy < 0:
            self.energy = 0
        current_index = self.DIRECTIONS.index(self.direction)
        self.direction = self.DIRECTIONS[(current_index + 1) % len(self.DIRECTIONS)]

    def jump(self, height):
        self.energy -= height * 2
        if self.energy < 0:
            self.energy = 0
        self.y += height
