from duplocloud.client import DuploClient
from duplocloud.errors import DuploError

def main():
  try:
    duplo = DuploClient.from_env()
    duplo.run()
  except DuploError as e:
    print(e)
    exit(e.code)

if __name__ == "__main__":
  main()
