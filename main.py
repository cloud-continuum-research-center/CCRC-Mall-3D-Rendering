from typing import Union, Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/api/")
async def upload_video(file: UploadFile):
    
    UPLOAD_DIR = "./data"
    
    
@app.post("/api/downloadvideo")
def download_video(vidio_uuid: str):
    