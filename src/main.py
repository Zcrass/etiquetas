from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routers import labels

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### include routers
app.include_router(labels.router, prefix="/api", tags=["build_labels"])
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import json
    import os
    import uvicorn
    config_file = "cfg/api_config.json"
    host = "localhost"
    port = 8000
    
    if os.path.exists(config_file):
        api_config = json.load(open(config_file))
        host = api_config.get("host", host)
        port = api_config.get("port", port)

    uvicorn.run(app, host=host, port=port)
