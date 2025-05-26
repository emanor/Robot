import unittest
from unittest.mock import patch

from robot import Robot
from game import Game

class TestRobot(unittest.TestCase):
    def test_robot_initialization_default(self):
        robot = Robot()
        self.assertEqual(robot.x, 0)
        self.assertEqual(robot.y, 0)
        self.assertEqual(robot.energy, 100)
        self.assertEqual(robot.direction, "EAST")

    def test_robot_initialization_custom(self):
        robot = Robot(x=10, y=20, energy=50)
        self.assertEqual(robot.x, 10)
        self.assertEqual(robot.y, 20)
        self.assertEqual(robot.energy, 50)
        self.assertEqual(robot.direction, "EAST") # Direction should still be default

    def test_turn_left(self):
        robot = Robot(energy=10)
        self.assertEqual(robot.direction, "EAST")
        
        robot.turn_left() # EAST -> NORTH
        self.assertEqual(robot.direction, "NORTH")
        self.assertEqual(robot.energy, 9)

        robot.turn_left() # NORTH -> WEST
        self.assertEqual(robot.direction, "WEST")
        self.assertEqual(robot.energy, 8)

        robot.turn_left() # WEST -> SOUTH
        self.assertEqual(robot.direction, "SOUTH")
        self.assertEqual(robot.energy, 7)

        robot.turn_left() # SOUTH -> EAST
        self.assertEqual(robot.direction, "EAST")
        self.assertEqual(robot.energy, 6)

    def test_turn_right(self):
        robot = Robot(energy=10)
        self.assertEqual(robot.direction, "EAST")

        robot.turn_right() # EAST -> SOUTH
        self.assertEqual(robot.direction, "SOUTH")
        self.assertEqual(robot.energy, 9)

        robot.turn_right() # SOUTH -> WEST
        self.assertEqual(robot.direction, "WEST")
        self.assertEqual(robot.energy, 8)

        robot.turn_right() # WEST -> NORTH
        self.assertEqual(robot.direction, "NORTH")
        self.assertEqual(robot.energy, 7)

        robot.turn_right() # NORTH -> EAST
        self.assertEqual(robot.direction, "EAST")
        self.assertEqual(robot.energy, 6)

    def test_move_forward(self):
        robot = Robot(x=0, y=0, energy=100)
        
        # Move EAST
        robot.move_forward(10)
        self.assertEqual(robot.x, 10)
        self.assertEqual(robot.y, 0)
        self.assertEqual(robot.energy, 90)

        # Change direction to NORTH
        robot.direction = "NORTH"
        robot.move_forward(5)
        self.assertEqual(robot.x, 10) # x should not change
        self.assertEqual(robot.y, 5)  # y should increase
        self.assertEqual(robot.energy, 85)

        # Change direction to WEST
        robot.direction = "WEST"
        robot.move_forward(7)
        self.assertEqual(robot.x, 3)  # x should decrease
        self.assertEqual(robot.y, 5)  # y should not change
        self.assertEqual(robot.energy, 78)

        # Change direction to SOUTH
        robot.direction = "SOUTH"
        robot.move_forward(3)
        self.assertEqual(robot.x, 3)  # x should not change
        self.assertEqual(robot.y, 2)  # y should decrease
        self.assertEqual(robot.energy, 75)

    def test_jump(self):
        robot = Robot(y=0, energy=50)
        robot.jump(10)
        self.assertEqual(robot.y, 10)
        self.assertEqual(robot.energy, 30) # 50 - (10 * 2)

        robot.jump(5)
        self.assertEqual(robot.y, 15)
        self.assertEqual(robot.energy, 20) # 30 - (5 * 2)

    def test_energy_depletion(self):
        robot = Robot(energy=5)
        robot.move_forward(10) # Energy cost is 10
        self.assertEqual(robot.energy, 0)
        self.assertEqual(robot.x, 10) # Still moves

        robot = Robot(energy=5)
        robot.jump(3) # Energy cost is 3 * 2 = 6
        self.assertEqual(robot.energy, 0)
        self.assertEqual(robot.y, 3) # Still jumps

        robot = Robot(energy=0)
        robot.move_forward(1)
        self.assertEqual(robot.energy, 0) # Should not go below 0

        robot = Robot(energy=1)
        robot.turn_left() # Cost 1
        self.assertEqual(robot.energy, 0)
        robot.turn_left() # Cost 1, but already 0
        self.assertEqual(robot.energy, 0)


class TestGame(unittest.TestCase):
    def setUp(self):
        # Suppress print output during tests unless specifically testing for it
        self.patcher = patch('builtins.print')
        self.mock_print = self.patcher.start()
        self.game = Game(width=10, height=10) # Smaller board for easier testing

    def tearDown(self):
        self.patcher.stop()

    def test_game_initialization(self):
        self.assertEqual(self.game.board_width, 10)
        self.assertEqual(self.game.board_height, 10)
        self.assertIsNotNone(self.game.robot)
        self.assertEqual(self.game.robot.x, 0)
        self.assertEqual(self.game.robot.y, 0)
        self.assertFalse(self.game.game_over)

    def test_update_state_boundary_conditions(self):
        # Test positive X boundary
        self.game.robot.x = 15
        self.game.update_state()
        self.assertEqual(self.game.robot.x, self.game.board_width - 1) # 9

        # Test negative X boundary
        self.game.robot.x = -5
        self.game.update_state()
        self.assertEqual(self.game.robot.x, 0)

        # Test positive Y boundary
        self.game.robot.y = 15
        self.game.update_state()
        self.assertEqual(self.game.robot.y, self.game.board_height - 1) # 9
        
        # Test negative Y boundary (after a jump, for example)
        # Robot's move_forward and jump directly modify y. update_state clamps it.
        self.game.robot.y = -5 
        self.game.update_state()
        self.assertEqual(self.game.robot.y, 0)

    def test_handle_input_move(self):
        initial_x = self.game.robot.x
        initial_energy = self.game.robot.energy
        self.game.handle_input("move 5")
        self.assertEqual(self.game.robot.x, initial_x + 5)
        self.assertEqual(self.game.robot.energy, initial_energy - 5)

    def test_handle_input_jump(self):
        initial_y = self.game.robot.y
        initial_energy = self.game.robot.energy
        self.game.handle_input("jump 3")
        self.assertEqual(self.game.robot.y, initial_y + 3)
        self.assertEqual(self.game.robot.energy, initial_energy - (3 * 2))

    def test_handle_input_turn_left(self):
        initial_direction = self.game.robot.direction
        initial_energy = self.game.robot.energy
        self.game.handle_input("turn left")
        self.assertNotEqual(self.game.robot.direction, initial_direction)
        self.assertEqual(self.game.robot.energy, initial_energy - 1)

    def test_handle_input_turn_right(self):
        initial_direction = self.game.robot.direction
        initial_energy = self.game.robot.energy
        self.game.handle_input("turn right")
        self.assertNotEqual(self.game.robot.direction, initial_direction)
        self.assertEqual(self.game.robot.energy, initial_energy - 1)

    def test_handle_input_quit(self):
        self.assertFalse(self.game.game_over)
        self.game.handle_input("quit")
        self.assertTrue(self.game.game_over)

    def test_handle_input_invalid_command(self):
        # Check that an invalid command doesn't crash and prints a message
        initial_x = self.game.robot.x
        initial_y = self.game.robot.y
        initial_energy = self.game.robot.energy
        
        self.game.handle_input("fly high")
        self.mock_print.assert_any_call("Unknown command: fly high")
        
        # Ensure robot state is unchanged
        self.assertEqual(self.game.robot.x, initial_x)
        self.assertEqual(self.game.robot.y, initial_y)
        self.assertEqual(self.game.robot.energy, initial_energy)

    def test_handle_input_invalid_move_argument(self):
        initial_x = self.game.robot.x
        self.game.handle_input("move abc")
        self.mock_print.assert_any_call("Invalid argument for command. Distance and height must be numbers.")
        self.assertEqual(self.game.robot.x, initial_x) # x should not change

    def test_handle_input_missing_argument_move(self):
        self.game.handle_input("move")
        self.mock_print.assert_any_call("Move command requires one argument: distance.")

    def test_handle_input_missing_argument_jump(self):
        self.game.handle_input("jump")
        self.mock_print.assert_any_call("Jump command requires one argument: height.")

    def test_handle_input_invalid_turn_argument(self):
        self.game.handle_input("turn around")
        self.mock_print.assert_any_call("Invalid turn command. Use 'turn left' or 'turn right'.")

    def test_game_over_on_energy_depletion(self):
        self.game.robot.energy = 5 # Low energy
        self.assertFalse(self.game.game_over)
        
        # Perform an action that consumes more than 5 energy
        self.game.handle_input("move 10") # Cost 10
        self.game.update_state() # update_state checks for energy depletion
        
        self.assertEqual(self.game.robot.energy, 0)
        self.assertTrue(self.game.game_over)
        self.mock_print.assert_any_call("Game Over: Robot out of energy")

    def test_commands_after_game_over(self):
        self.game.game_over = True
        initial_x = self.game.robot.x
        self.game.handle_input("move 5")
        self.mock_print.assert_any_call("Game is over. Cannot accept further commands.")
        self.assertEqual(self.game.robot.x, initial_x) # Robot should not move


if __name__ == '__main__':
    unittest.main()
