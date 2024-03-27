from duplocloud.client import DuploClient
from duplocloud.resource import DuploTenantResourceV3
from duplocloud.commander import Resource

@Resource("secret")
class DuploSecret(DuploTenantResourceV3):
  
  def __init__(self, duplo: DuploClient):
    super().__init__(duplo, "k8s/secret")

  def name_from_body(self, body):
    return body["SecretName"]
