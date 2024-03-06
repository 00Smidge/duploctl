import os
import pytest 
import unittest

from .errors import DuploError
from .client import DuploClient
from pathlib import Path

# current working directory as variable
cwd = os.getcwd()
host = "http://example.duplocloud.net"
cache_dir = f"{cwd}/.tmp/cache"

def test_new_config():
  c = DuploClient(host=host)
  assert c.host == host

def test_at_least_host():
  duplo = DuploClient()
  # raises an error if host is not set
  with pytest.raises(DuploError) as e:
    duplo.token
    print(e)

def test_cache_dir():
  c = DuploClient(
    host=host,
    cache_dir=cache_dir)
  assert c.cache_dir == cache_dir
  random_data = {"foo": "bar"}
  cf = f"{cache_dir}/test.json"
  c.set_cached_item("test", random_data)
  assert os.path.exists(cf), f"Cache file {cf} not found"
  # now check if we can get the data back
  assert c.get_cached_item("test") == random_data, "Cached data does not match"
  # delete the cache file
  os.remove(cf)
  os.rmdir(cache_dir)
