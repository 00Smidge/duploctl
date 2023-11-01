from duplocloud.client import DuploClient
from duplocloud.resource import DuploTenantResource
from duplocloud.errors import DuploError
from duplocloud.commander import Command, Resource
import duplocloud.args as args

@Resource("service")
class DuploService(DuploTenantResource):
  
  def __init__(self, duplo: DuploClient):
    super().__init__(duplo)
  
  @Command()
  def list(self):
    """Retrieve a list of all services in a tenant."""
    tenant_id = self.tenant["TenantId"]
    return self.duplo.get(f"subscriptions/{tenant_id}/GetReplicationControllers")
  
  @Command()
  def find(self, 
           name: args.NAME):
    """Find a service by name.
    
    Args:
      name (str): The name of the service to find.
    Returns: 
      The service object.
    Raises:
      DuploError: If the service could not be found.
    """
    try:
      return [s for s in self.list() if s["Name"] == name][0]
    except IndexError:
      raise DuploError(f"Service '{name}' not found", 404)

  @Command()
  def update_image(self, 
                   name: args.NAME, 
                   image: args.IMAGE):
    """Update the image of a service.
    
    Args:
      name (str): The name of the service to update.
      image (str): The new image to use for the service.
    """
    tenant_id = self.tenant["TenantId"]
    service = self.find(name)
    allocation_tags = service["Template"]["AllocationTags"]
    data = {
      "Name": name,
      "Image": image,
      "AllocationTags": allocation_tags
    }
    self.duplo.post(f"subscriptions/{tenant_id}/ReplicationControllerChange", data)
    return {"message": f"Successfully updated image for service '{name}'"}
  
  @Command()
  def restart(self, 
              name: args.NAME):
    """Restart a service.
    
    Args:
      name (str): The name of the service to restart.
    Returns: 
      A success message if the service was restarted successfully.
    Raises:
      DuploError: If the service could not be restarted.
    """
    tenant_id = self.tenant["TenantId"]
    res = self.duplo.post(f"subscriptions/{tenant_id}/ReplicationControllerReboot/{name}")
    return {"message": f"Successfully restarted service '{name}'"}