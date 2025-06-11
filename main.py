from fastapi import FastAPI
from router import register_routes

app = FastAPI()
register_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


