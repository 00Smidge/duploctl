from .types import Arg
import os
from .commander import available_resources

# the global args for the CLI
HOST = Arg('host', '-H', 
            help='The tenant to be scope into',
            default=os.getenv('DUPLO_HOST', None))

TOKEN = Arg('token', '-p', 
            help='The token/password to authenticate with',
            default=os.getenv('DUPLO_TOKEN', None))

TENANT = Arg("tenant", "-t",
             help='The tenant name',
             default=os.getenv('DUPLO_TENANT', "default"))

OUTPUT = Arg("output", "-o",
              help='The output format',
              default=os.getenv('DUPLO_OUTPUT', 'json'))

# The rest are resource level args for commands
SERVICE = Arg('service', 
              help='The service to run',
              choices=available_resources())

COMMAND = Arg('command', 
             help='The subcommand to run')

NAME = Arg("name", 
           help='The resource name')

IMAGE = Arg("image", 
            help='The image to use')

SCHEDULE = Arg("schedule","-s", 
               help='The schedule to use')

ENABLE = Arg("enable","-y", 
              help='Enable or disable the feature',
              type=bool,
              action='store_true')
