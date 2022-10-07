from fastapi import APIRouter

route_hello = APIRouter()


@route_hello.get("/hello-world")
async def hello_world():
    return {"message": "Hello World"}