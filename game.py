from robot import Robot

class Game:
    def __init__(self, width=20, height=20):
        self.board_width = width
        self.board_height = height
        # Pass the game instance to the robot for potential future access to game state/rules
        self.robot = Robot(x=0, y=0, energy=100, game=self)
        self.game_over = False

    def start_game(self):
        print("Welcome to the Robot Game!")
        print("Commands: move <distance>, jump <height>, turn left, turn right, quit")

    def handle_input(self, command_str):
        if self.game_over:
            print("Game is over. Cannot accept further commands.")
            return

        parts = command_str.lower().split()
        if not parts:
            print("No command entered.")
            return

        command = parts[0]
        args = parts[1:]

        try:
            if command == "move":
                if len(args) == 1:
                    distance = int(args[0])
                    self.robot.move_forward(distance)
                else:
                    print("Move command requires one argument: distance.")
            elif command == "jump":
                if len(args) == 1:
                    height = int(args[0])
                    self.robot.jump(height)
                else:
                    print("Jump command requires one argument: height.")
            elif command == "turn":
                if len(args) == 1:
                    if args[0] == "left":
                        self.robot.turn_left()
                    elif args[0] == "right":
                        self.robot.turn_right()
                    else:
                        print("Invalid turn command. Use 'turn left' or 'turn right'.")
                else:
                    print("Turn command requires one argument: 'left' or 'right'.")
            elif command == "quit":
                self.game_over = True
                print("Quitting game.")
            else:
                print(f"Unknown command: {command_str}")
        except ValueError:
            print("Invalid argument for command. Distance and height must be numbers.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def update_state(self):
        if self.game_over:
            return

        # Boundary checks
        if self.robot.x < 0:
            self.robot.x = 0
        elif self.robot.x >= self.board_width:
            self.robot.x = self.board_width - 1

        if self.robot.y < 0:
            self.robot.y = 0
        elif self.robot.y >= self.board_height:
            self.robot.y = self.board_height - 1
        
        # Clamp y coordinate for jump (cannot go below ground)
        # Assuming ground is y=0, robot cannot jump into negative y if it started at y=0 or above
        # This specific behavior might need more clarification if robot can start below y=0
        # For now, if a jump results in y < 0, it's clamped to 0.
        if self.robot.y < 0 : # This check might be redundant if y starts at 0 and only increases with jump
             self.robot.y = 0


        if self.robot.energy <= 0:
            self.robot.energy = 0 # Ensure energy doesn't go negative in display
            print("Game Over: Robot out of energy")
            self.game_over = True

    def display_state(self):
        print(f"Robot position: ({self.robot.x}, {self.robot.y}), Direction: {self.robot.direction}")
        print(f"Robot energy: {self.robot.energy}")
        if self.game_over and self.robot.energy <= 0 :
             print("Status: Robot is out of energy!")
        elif self.game_over:
             print("Status: Game has been quit.")


        for r in range(self.board_height -1, -1, -1): # Print from top to bottom
            row_display = []
            for c in range(self.board_width):
                if self.robot.x == c and self.robot.y == r:
                    row_display.append("R")
                else:
                    row_display.append(".")
            print(" ".join(row_display))
        print("-" * (self.board_width * 2 -1)) # Separator line

    def run(self):
        self.start_game()
        while not self.game_over:
            self.display_state()
            command = input("Enter command: ")
            self.handle_input(command)
            self.update_state()
        
        # Final display after game over (e.g., after "quit" or out of energy)
        self.display_state() 
        print("Thanks for playing!")

if __name__ == "__main__":
    game = Game()
    game.run()
