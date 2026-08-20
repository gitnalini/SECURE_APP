import pika
import json
from datetime import datetime, timezone



def publish_event(event_type, vendor_id, status, data):
    try:
        connection =pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel=connection.channel()
        channel.queue_declare(queue='license_events',durable=True)
        message_payload={
            "event_type": event_type,
            "vendor_id":vendor_id,
            "status":status,
            "data":data, 
            "time":datetime.now(timezone.utc).isoformat(),
        }
        message=json.dumps(message_payload)
        channel.basic_publish(exchange='',
                              routing_key='license_events',
                              body=message)

    except Exception as e:
        print(f"Telemetry publish failed: {e}")