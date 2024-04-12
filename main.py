from typing import Union, Annotated

from fastapi import FastAPI, File, UploadFile, BackgroundTasks
import aws_module
import rendering_module
import time
from multiprocessing import Process, Queue
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
    
    
@app.put("/api/downloadvideo")
def download_video(video_uuid: str, backgroundTasks: BackgroundTasks):
    aws_module.download_file(video_uuid, "3d-modeling-mall", video_uuid)
    # sfm_process = Process(target=rendering_module.sfm_runner, args=(video_uuid,))
    # sfm_process.start()
    # sfm_process.join()
    backgroundTasks.add_task(rendering_module.sfm_runner, video_uuid)
    
# @app.put("/api/downloadvideo")
# def download_video(video_uuid: str):
#     time.sleep(5)
    
#     print("is thread clear?", video_uuid)