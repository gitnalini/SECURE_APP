import requests   
import time
from prometheus_client.parser import text_string_to_metric_families
 


def metrics_to_grafana():

    # getting the metrics from the endpoint
    response = requests.get("https://securekey-8s49.onrender.com/metrics")
    metrics = response.text  # why this is because the response is in bytes format, we need to decode it to string format
    current_timestamp_ms = int(time.time() * 1000)
    parsed_metrics=[]

    # turning the metrics into a list of metric families 
    for family in text_string_to_metric_families(metrics):
     
        for sample in family.samples:
            parsed_metrics.append({
                "metric":{
                    "__name__":sample.name,
                    **sample.labels
                },
                "values":[sample.value],
                "timestamps":[current_timestamp_ms]
            })
        
    return parsed_metrics
