from typing import Union, Annotated

from fastapi import FastAPI, File, UploadFile, BackgroundTasks
import aws_module
import rendering_module
import time
from multiprocessing import Process, Queue
from pydantic import BaseModel

class VideoInfo(BaseModel):
    item_id : int
    video_uuid : str
    




app = FastAPI()

@app.get("/api")
def test():
    return True


    
@app.post("/api/downloadvideo")
def download_video(video_info : VideoInfo, backgroundTasks: BackgroundTasks):
    aws_module.download_file(video_info.video_uuid, "3d-modeling-mall", video_info.video_uuid)
    # sfm_process = Process(target=rendering_module.sfm_runner, args=(video_uuid,))
    # sfm_process.start()
    # sfm_process.join()
    backgroundTasks.add_task(rendering_module.sfm_runner, video_info.video_uuid, video_info.item_id)
    