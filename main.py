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
    db=0,
)


# models
class Product(HashModel):
    name: str
    price: float
    quantity: int

    # connect with redis
    class Meta:
        database = redis


# views
@app.get('/products')
def all():
    return Product.all_pks()


@app.get("/")
async def root():
    return {"message": "Hello World"}
