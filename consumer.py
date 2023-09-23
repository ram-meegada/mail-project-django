import pika, json, os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mail_project.settings")
django.setup()
from django.conf import settings
from api.models import User

def callback(ch, method, properties, body):
    # Process the incoming message
    body = json.loads(body)
    print(f"Received message:", body)
    if properties.content_type == "user_created":
        user = User(email=body['email'], username=body['username'])
        user.set_password(body['password'])
        user.save()
        print('created***********')
    elif properties.content_type == "user_details_updated":
        user = User.objects.get(email = body['email'])
        user.email = body['email']
        user.username = body['username']
        user.save()
        print('updated***********')
    elif properties.content_type == "user_deleted":
        user = User.objects.get(user_id = body['id'])
        user.delete()
        print('deleted***********')

def consume_messages():
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

    # Create a channel
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='django_project2')

    # Set up a message consumer
    channel.basic_consume(queue='django_project2', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. MAIL_PROJECT*******************')
    channel.start_consuming()

# Example usage:
consume_messages()