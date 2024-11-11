# security/firewall_rules.sh
#!/bin/bash
# Firewall setup script

# Allow SSH
ufw allow ssh

# Allow HTTP and HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Allow Prometheus and Grafana
ufw allow 9090/tcp
ufw allow 3000/tcp

# Allow Elasticsearch and Kibana
ufw allow 9200/tcp
ufw allow 5601/tcp

# Enable UFW
ufw enable
