from .Position import Position
from .Config import Config
from .Utils import Try


@Try.catch
class Rover:

    def __init__(self, rover_name, plateau, position, heading):
        """Initializing mars rover with below params

        Args:
            rover_name (str): _description_
            plateau (class): _description_
            position (class): _description_
            heading (int): _description_
        """
        self.rover_name = rover_name
        self.plateau = plateau
        self.position = position
        self.heading = heading
        self.available_commands = Config.COMMANDS
        self.available_directions = Config.DIRECTIONS

    def current_position(self):
        """ Final current position of the Rover

        Returns:
            str: Final current position of the Rover
        """
        self.plateau.create_obstace(self.position.x, self.position.y)
        return f'{self.rover_name}:{self.position.x} {self.position.y} {self.get_heading}'

    @property
    def get_heading(self):
        """ Get the rover heading direction

        Returns:
            str: Direction (N, S, E, W)
        """
        directions = list(self.available_directions.keys())

        try:
            direction = directions[self.heading - 1]
        except IndexError:
            direction = 'N'
            print('Direction error...')

        return direction


    def run(self, commands):
        """ Run final Rover commands

        Args:
            commands (str): Commands, Ex: LMLMLMLMM

        Raises:
            Exception: If invalid command
        """

        for command in commands:
            if self.plateau.check_if_position_reserved(self.position.x, self.position.y):
                raise Exception("This position is reserved by another Rover")
            
            cmd = self.available_commands.get(command, None)
            if cmd:
                getattr(self, cmd)()
            else:
                raise Exception(f"Invalid command {command}")

    def move(self):
        """ Rover Move forward handler

        Returns:
            Bool: Bool
        """
        if not self.plateau.move_available(self.position):
            raise Exception("Cannot move further")
        # Assume that the square directly North from (x, y) is (x, y+1).
        if self.available_directions['N'] == self.heading:
            self.position.y += 1
        elif self.available_directions['E'] == self.heading:
            self.position.x += 1
        elif self.available_directions['S'] == self.heading:
            self.position.y -= 1
        elif self.available_directions['W'] == self.heading:
            self.position.x -= 1

        return True

    def turn_left(self):
        """ 
        Rover turn Left
        """
        
        if (self.heading - 1) < self.available_directions['N']:
            self.heading = self.available_directions['W']
        else:
            self.heading -= 1

    def turn_right(self):
        """ 
        Rover turn Right
        """
        
        if (self.heading + 1) > self.available_directions['W']:
            self.heading = self.available_directions['N']
        else:
            self.heading += 1
