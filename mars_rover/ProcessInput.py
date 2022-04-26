from enum import Enum
import re
from .Config import Config
from .Utils import Try

@Try.catch
class ProcessInput:

    def __init__(self, command_callback, input_filename):
        self.command_callback = command_callback
        self.input_filename = input_filename
        self.current_state = ProcessInput.PlateauConfigState(command_callback)

    def parse_file(self):
        with open(self.input_filename, encoding='utf-8') as input_file:
            for each_line in input_file:
                yield each_line

    def start(self):
        for input_line in self.parse_file():
            result = self.current_state.parse_string(input_line.strip())
            self.transition_state(result)

    def transition_state(self, current_state_result):
        invalid_result = False
        if type(self.current_state) is ProcessInput.PlateauConfigState:
            if current_state_result is ProcessInput.ParseState.Result.SUCCESS:
                self.current_state = ProcessInput.RoverLandingState(
                    self.command_callback)
            elif current_state_result is ProcessInput.ParseState.Result.FAIL:
                raise ProcessInput.BadFileFormatError()
            else:
                invalid_result = True
        elif type(self.current_state) is ProcessInput.RoverLandingState:
            if current_state_result is ProcessInput.ParseState.Result.SUCCESS:
                input_args = [self.current_state.get_name()] + \
                    list(self.current_state.get_config())
                self.current_state = ProcessInput.RoverInstructionsState(
                    self.command_callback, tuple(input_args))
            elif current_state_result is not ProcessInput.ParseState.Result.FAIL:
                invalid_result = True
        elif type(self.current_state) is ProcessInput.RoverInstructionsState:
            if (current_state_result is ProcessInput.ParseState.Result.SUCCESS or
                    current_state_result is ProcessInput.ParseState.Result.FAIL):
                self.current_state = ProcessInput.RoverLandingState(
                    self.command_callback)
            else:
                invalid_result = True

        if invalid_result is True:
            raise ValueError(f'Invalid state_result {current_state_result} for state {type(self.current_state)}.')
        
    class BadFileFormatError(BaseException):
        pass

    class ParseState:
        class Result(Enum):
            FAIL = -1
            SUCCESS = 0

        def __init__(self, command_callback):
            self._command_callback = command_callback

    class PlateauConfigState(ParseState):
        class Commands(Enum):
            CREATE_PLATEAU = 0

        def parse_string(self, input_string):
            match_regex = re.compile(Config.PLATEAU_CFG_FORMAT)
            match_result = match_regex.match(input_string)
            if match_result is None:
                return self.Result.FAIL
            max_x_coord, max_y_coord = int(
                match_result.group(1)), int(match_result.group(2))
            self._command_callback(
                self.Commands.CREATE_PLATEAU, max_x_coord, max_y_coord)
            return self.Result.SUCCESS

    class RoverLandingState(ParseState):
        def __init__(self, command_callback):
            super(ProcessInput.RoverLandingState,
                  self).__init__(command_callback)
            self._config = None
            self._name = None

        def get_config(self):
            return self._config

        def get_name(self):
            return self._name

        def parse_string(self, input_string):
            match_regex = re.compile(Config.ROVER_INPUTS_FORMAT['landing'])
            match_result = match_regex.match(input_string)
            if match_result is None:
                return self.Result.FAIL
            self._name = match_result.group(1)
            self._config = int(match_result.group(2)), int(
                match_result.group(3)), match_result.group(4)
            return self.Result.SUCCESS

    class RoverInstructionsState(ParseState):
        class Commands(Enum):
            CREATE_ROVER = 0

        def __init__(self, command_callback, rover_config):
            super(ProcessInput.RoverInstructionsState,
                  self).__init__(command_callback)
            self._rover_config = rover_config

        def parse_string(self, input_string):
            match_regex = re.compile(
                Config.ROVER_INPUTS_FORMAT['instructions'])
            match_result = match_regex.match(input_string)
            rover_name = self._rover_config[0]
            if match_result is None or match_result.group(1) != rover_name:
                return self.Result.FAIL
            callback_commands = [self.Commands.CREATE_ROVER] + \
                list(self._rover_config) + [match_result.group(2)]
            self._command_callback(*callback_commands)
            return self.Result.SUCCESS
