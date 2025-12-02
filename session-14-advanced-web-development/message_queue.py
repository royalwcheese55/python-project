from fastapi import FastAPI
from celery import Celery
import uuid
from .message_consumer import process_order

app_celery = Celery(
    'orders',
    broker='amqp://localhost',
    backend='rpc://'
)

app_celery.conf.update(
    task_serializer="json",
    accept_content=['json'],  # Ignore other content
    result_serializer='json'
)

app = FastAPI()




@app.post('/orders')
def create_order(customer: str, amount: float):
    order_id = str(uuid.uuid4())[:10]
    task = process_order.delay(order_id, customer, amount)
    
    return {
        'status': 'processing',
        'order_id': order_id,
        'task_id': task.id
    }
    
    