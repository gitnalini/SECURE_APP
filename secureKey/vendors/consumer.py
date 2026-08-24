import pika
import json
import os
import django 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','securekey.settings')
django.setup()

from vendors.models import ValidationLog, Vendor

 

def callback(ch, method, properties, body):
    try:
        event=json.loads(body)
        vendor_id=event['vendor_id']
        vendor=Vendor.objects.get(id=vendor_id)
        data = event['data']

        ValidationLog.objects.create(
            vendor=vendor,
            event_type=event['event_type'],
            status=event['status'],
            license_key=data.get('license_key'),
            fingerprint=data.get('fingerprint'),
            expiry=data.get('expiry'),
            timestamp=event['time']
        )
        print(f"[✓] Logged event: {event['event_type']} - {event['status']}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[✗] Failed to log event: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)



def main():
    url=os.environ.get('RABBITMQ_URL','amqp://guest:guest@localhost:5672/')
    connection=pika.BlockingConnection(pika.URLParameters(url))
    channel=connection.channel()
    channel.queue_declare(queue='license_events', durable=True)
    channel.basic_consume(queue='license_events', on_message_callback=callback,auto_ack=False)
    print('[*] Waiting for telemetry events. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()