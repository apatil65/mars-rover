class Config:

    COMMANDS = {
        'M': 'move',
        'L': 'turn_left',
        'R': 'turn_right'
    }

    DIRECTIONS = {
        'N': 1,
        'E': 2,
        'S': 3,
        'W': 4,
    }

    ROVER_INPUTS_FORMAT = {
        'landing': '^([a-zA-Z0-9]*\w)\s+Landing:([0-9]+)\s+([0-9]+)\s+(\w)$',
        'instructions': '^([a-zA-Z0-9]*\w)\s+Instructions:\s*(\w+)$'
    }

    PLATEAU_CFG_FORMAT = '^Plateau:([0-9]+)\s+([0-9]+)$'
