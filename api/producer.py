import pika
from django.conf import settings

def publish_message(message):
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=pika.PlainCredentials(
                'ram', 'ram'
            ),
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue='mail_project')

    # Publish the message
    channel.basic_publish(exchange='', routing_key='mail_project', body=message)

    # Close the connection
    connection.close()

# Example usage:
# message = "Hello, RabbitMQ!"
# publish_message(message)
