from starlette.requests import Request
import requests as requests
from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)

redis = get_redis_connection(
    host='localhost',
    port=6379,
    password="password",
    decode_responses=True,
    db=1,
)


class Order(HashModel):
    product_id: str
    price: float
    fees: float
    total: float
    quantity: int
    status: str  # pending, completed and refundend

    class Meta:
        database = redis


@app.post("/orders")
async def create(request: Request):
    body = await request.json()

    req = requests.get('http://127.0.0.1:8000/products/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()
    return order
