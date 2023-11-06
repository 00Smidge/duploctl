import inspect 
import argparse
from importlib.metadata import entry_points
from .errors import DuploError
from .types import Arg

ENTRYPOINT="duplocloud.net"
FORMATS=f"formats.{ENTRYPOINT}"
ep = entry_points(group=ENTRYPOINT)
fep = entry_points(group=FORMATS)
schema = {}
resources = {}

def Resource(name: str):
  def decorator(cls):
    resources[name] = {
      "class": cls.__qualname__
    }
    return cls
  return decorator

def Command():
  """Command decorator

  This decorator is used to register a function as a command. It will
  automatically generate the command line arguments for the function
  based on the annotations.

  Example:
    ```python
    from duplocloud.commander import Command
    from duplocloud import args
    @Command()
    def hello(name: args.NAME = "world"):
      print(f"Hello {name}!")
    ```
  
  Returns:
    The decorated function.

  """
  def decorator(function):
    sig = inspect.signature(function)
    def arg_anno(name, param):
      if not param.annotation.positional and name != param.annotation.__name__:
        param.annotation.set_attribute("dest", name)
      if param.default is not inspect.Parameter.empty:
        param.annotation.set_attribute("default", param.default)
      return param.annotation
    schema[function.__qualname__] = [
        arg_anno(k, v)
        for k, v in sig.parameters.items()
        if v.annotation is not inspect.Parameter.empty and isinstance(v.annotation, Arg)
    ]
    return function
  return decorator

def get_parser(function):
  qn = function.__qualname__
  parser = argparse.ArgumentParser(
    prog='duplocloud-cli',
    description='Duplo Cloud CLI',
  )
  try:
    for arg in schema[qn]:
      parser.add_argument(*arg.flags, **arg.attributes)
  except KeyError:
    raise DuploError(f"Function named {qn} not registered as a command.", 3)
  return parser

def apply_args(function, parser):
  qn = function.__qualname__
  try:
    for arg in schema[qn]:
      parser.add_argument(*arg.flags, **arg.attributes)
  except KeyError:
    raise DuploError(f"Function named {qn} not registered as a command.", 3)
  return parser

def load_service(name: str):
  """Load Service
    
  Load a Service class from the entry points.

  Args:
    name: The name of the service.
  Returns:
    The class of the service.
  """
  return ep[name].load()

def load_format(name: str="string"):
  """Load Format
    
  Load a Formatter function from the entry points.

  Args:
    name: The name of the format.
  Returns:
    The class of the format.
  """
  return fep[name].load()

def available_resources():
  """Available Resources

  Returns:
    A list of available resources names.
  """
  return list(ep.names)
