from fastapi import FastAPI
import httpx

from my_module import hello
from packages.my_class import MyClass
from packages.my_function import add

hello_patea = MyClass("Patea").hello()
sum = add(12, 34)

app = FastAPI()

@app.get("/")
async def get_root():
    response: dict[str, object] = {
        "hello": hello(),
        "sum": sum,
        "hello_patea": hello_patea
    }
    return response

@app.get("/exchange-rates")
async def get_exchange_rattes():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
    return data
