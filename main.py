from fastapi import FastAPI
from redis_om import get_redis_connection

app = FastAPI()

redis = get_redis_connection(
    host='localhost',
    port=6379,
    password="password",
    decode_responses=True,
    db=0,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}