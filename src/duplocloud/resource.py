from .client import DuploClient
from .errors import DuploError
from .commander import get_parser

class DuploResource():
  
  def __init__(self, duplo: DuploClient):
    self.duplo = duplo
    self.tenant = None
  
  def command(self, name):
    if not (command := getattr(self, name, None)):
      raise DuploError(f"Invalid command: {name}")
    return command
  
  def exec(self, cmd, args=[]):
    try:
      command = self.command(cmd)
      parser = get_parser(command.__qualname__)
      parsed_args = parser.parse_args(args)
      res = command(**vars(parsed_args))
      # if res is a dict or list, turn it into json
      if isinstance(res, (dict, list)):
        res = self.duplo.json(res)
      return print(res)
    except DuploError as e:
      raise e
    except Exception as e:
      raise DuploError(f"Error executing subcommand: {cmd}") from e
    
class DuploTenantResource(DuploResource):
  def __init__(self, duplo: DuploClient):
    self.duplo = duplo
    self.tenant = None
    self.tenent_svc = duplo.service('tenant')
  def get_tenant(self):
    if not self.tenant:
      self.tenant_svc = self.duplo.service("tenant")
      self.tenant = self.tenant_svc.find(self.duplo.tenant_name)
    return self.tenant
