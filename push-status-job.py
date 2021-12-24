import gevent
import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# 1 true or 0 false
value_cisco_3000='1'
value_cisco_5000='0'


registry = CollectorRegistry()
g = Gauge('job_backup_config_cisco_3000', 'Last time a batch job successfully finished', registry=registry)
g.set(value_cisco_3000)
push_to_gateway('192.168.1.2:9091', job='cisco_3000', registry=registry)

g = Gauge('job_backup_config_cisco_5000', 'Last time a batch job successfully finished', registry=registry)
g.set(value_cisco_5000)
push_to_gateway('192.168.1.2:9091', job='cisco_5000', registry=registry)
