import time

from PIL import Image
from fastapi import FastAPI, Path, HTTPException, UploadFile, responses
from fastapi.openapi.models import Response
from starlette.requests import Request
from starlette.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from deta import Drive, Deta
import os

from primeNumbers import *
from invertPhoto import *

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/prime/{number}")
async def read_item(
        number: int = Path(
            description="The number to check if it is prime or not",
            gt=0,
            lt=922332036854775807
        )
):
    return check_if_prime(number)


@app.post("/upload-photo")
async def read_item(file: UploadFile = File(..., format=".jpeg")):
    if len(await file.read()) >= 12000000:
        raise HTTPException(status_code=413, detail="Image is greater than 12MB")
    #if file.content_type != "image/jpeg":
       # raise HTTPException(status_code=400, detail="File content type must be jpg")
    save_image(file, file.filename)
    move_image(file.filename)
    return {"name_of_file": file.filename}


@app.get("/picture/invert/{filename}", response_class=HTMLResponse)
async def read_item(request: Request, filename: str = Path(
    description="The name of the file"
)):
    out = []
    for filename in os.listdir("images"):
        out.append({
            "name": filename.split(".")[0],
            "path": "/images" + filename
        }
        )
        return out

    # wait_time = 0.5
    # time.sleep(wait_time)
    # print('images/' + filename)
    # img = Image.open('images/'+filename)
    # return Response(content=img, media_type="image/jpeg")
