import sys
from mars_rover.Plateau import Plateau
from mars_rover.Position import Position
from mars_rover.Rover import Rover
from mars_rover.ProcessInput import ProcessInput
from mars_rover.Config import Config
from mars_rover.Utils import Try


@Try.catch
def command_interpreter(command, *args):
    """ Command interpreter callback

    Args:
        command (str): command type
    """
    global plateau
    if command is ProcessInput.PlateauConfigState.Commands.CREATE_PLATEAU:
        plateau = Plateau(args[0], args[1])
    elif command is ProcessInput.RoverInstructionsState.Commands.CREATE_ROVER:
        rover_name = args[0]
        rover_position = tuple(args[1:3])
        rover_bearing = args[3]
        rover_instructions = args[4]

        position = Position(rover_position[0], rover_position[1])
        rover = Rover(rover_name, plateau, position,
                      Config.DIRECTIONS.get(rover_bearing))
        rover.run(rover_instructions)
        print(rover.current_position())

@Try.catch
def process_input(input_filename):
    process = ProcessInput(command_interpreter, input_filename)
    process.start()

@Try.catch
def main():
    if len(sys.argv) < 2:
        raise Exception("Syntax: python driver.py <input_filename>")
    process_input(sys.argv[1])


if __name__ == "__main__":
    main()
