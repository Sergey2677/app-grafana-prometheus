from fastapi import FastAPI, status
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()



@app.get('/')
async def hello():
    for i in range(1, 10000):
        pass
    return "Hello world"

@app.get('/health')
async def health():
    return status.HTTP_200_OK

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

