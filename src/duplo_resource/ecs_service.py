from duplocloud.client import DuploClient
from duplocloud.resource import DuploTenantResource
from duplocloud.errors import DuploError
from duplocloud.commander import Command, Resource
import duplocloud.args as args


@Resource("ecs_service")
class DuploEcsService(DuploTenantResource):

    def __init__(self, duplo: DuploClient):
        super().__init__(duplo)

    @Command()
    def list(self):
        """Retrieve a list of all ECS services in a tenant."""
        tenant_id = self.tenant["TenantId"]
        url = f"v3/subscriptions/{tenant_id}/aws/ecs/service"
        response = self.duplo.get(url)
        return response.json()

    @Command()
    def find(self, name: args.NAME):
        """Find a ECS service by name.

        Args:
          name (str): The name of the ECS service to find.
        Returns:
          The ECS service object.
        Raises:
          DuploError: If the ECS service could not be found.
        """

        try:
            return [s for s in self.list() if s["DuploEcsService"]["Name"] == name][0]
        except IndexError:
            raise DuploError(f"ECS Service '{name}' not found", 404)

    @Command()
    def update(self, name: args.NAME, task_definition: args.IMAGE):
        """Update the image for an ECS service.

        Args:
          name (str): The name of the ECS service to update.
          task_definition (str): The new task definition to use.
        Returns:
          The updated ECS object.
        Raises:
            DuploError: If the ECS service could not be updated.
        """
        tenant_id = self.tenant["TenantId"]
        ecs_service = {
            "Name": name,
            "TaskDefinition": task_definition
        }

        try:
            self.duplo.post(
                f"subscriptions/{tenant_id}/UpdateEcsService",
                ecs_service)
        except Exception as e:
            raise DuploError(f"Failed to update ECS Service '{name}': {e}")

        return self.find(name)
