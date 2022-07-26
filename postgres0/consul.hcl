# location /etc/consul.d/consul.hcl
bind_addr = "192.168.56.109"
client_addr = "192.168.56.109"
datacenter = "dc1"
data_dir = "/opt/consul"
retry_join = ["192.168.56.108","192.168.56.106","192.168.56.107"]
