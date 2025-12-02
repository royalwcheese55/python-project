from celery import Celery
import time
import redis

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

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


@app_celery.task(
    name='process_order',
    autoretry_for=(Exception, ),
    retry_kwargs={'max_retries': 3},
    retry_backoff=True
)
# idempotency
def process_order(order_id, customer, amount):
    time.sleep(2)

    # handle idempotency

    processed = redis_client.get(order_id)
    
    if processed:
        # already processed
        return 
    
    result = {
        'order_id': order_id,
        'customer': customer,
        'amount': amount,
        'status': 'completed'
    }  

    redis_client.set(order_id, "processed")
    
    
    print(f'Order {order_id} processed complete')
    return result

