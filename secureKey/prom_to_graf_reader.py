import base64
import time
import os
from prometheus_remote_writer import RemoteWriter
from prom_to_grafana import metrics_to_grafana


 
username = "3562378"
password = os.environ.get('GRAFANA_API_TOKEN')
auth_string = f"{username}:{password}"
encoded = base64.b64encode(auth_string.encode()).decode()
headers = {"Authorization": f"Basic {encoded}"}
current_timestamp_ms = int(time.time() * 1000)

# Create a RemoteWriter instance
writer = RemoteWriter(
    url="https://prometheus-prod-43-prod-ap-south-1.grafana.net/api/prom/push",
    headers = {"Authorization": f"Basic {encoded}"}
)

# Prepare the data to send
data = metrics_to_grafana()

# Send the data
writer.send(data)
