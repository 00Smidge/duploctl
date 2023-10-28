from .types import Arg
import os

HOST = Arg('host', '-H', 
            help='The tenant to be scope into',
            default=os.getenv('DUPLO_HOST', None))

TOKEN = Arg('token', '-p', 
            help='The token/password to authenticate with',
            default=os.getenv('DUPLO_TOKEN', None))

TENANT = Arg("tenant", "-t",
             help='The tenant name',
             default=os.getenv('DUPLO_TENANT', None))

SERVICE = Arg('service', 
              help='The service to run')

COMMAND = Arg('command', 
             help='The subcommand to run')

NAME = Arg("name", 
           help='The resource name')

IMAGE = Arg("image", 
            help='The image to use')

SCHEDULE = Arg("schedule","-s", 
               help='The schedule to use')

ENABLE = Arg("enable","-y", 
              help='Enable or disable the feature')
