import time

from redis_om import get_redis_connection

redis = get_redis_connection(
    host='localhost',
    port=6379,
    password="password",
    decode_responses=True,
    db=1,
)

key = 'order_completed'
group = 'inventory-group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        print(results)

    except Exception as e:
        print(str(e))
    time.sleep(1)
