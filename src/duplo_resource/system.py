import datetime
from duplocloud.client import DuploClient
from duplocloud.resource import DuploResource
from duplocloud.errors import DuploError

class DuploSystem(DuploResource):
  def __init__(self, duplo: DuploClient):
    super().__init__(duplo)
  
  def info(self):
    """Retrieve all of the system information."""
    return self.duplo.get("v3/features/system")
  