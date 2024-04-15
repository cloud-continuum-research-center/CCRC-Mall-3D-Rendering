from typing import Union, Annotated
import json
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Response
import aws_module
import rendering_module
import time
from multiprocessing import Process, Queue
from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

class VideoInfo(BaseModel):
    item_id : int
    video_uuid : str
    
class ProgInfo(BaseModel):
    prog_num : int
    elapsed : float
    remain : float



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
    
@app.get("/api/proginfo")
def get_proginfo():
    with open("progress_log/"+"test"+"_progress.json", 'r') as file:
        data = json.load(file)
        #datas = []
        #datas.append(data)
        #print(datas)
        json_str = json.dumps(data)
        return Response(content=json_str, media_type='application/json')
    