from fastapi import FastAPI, Path, UploadFile

from starlette.requests import Request
from starlette.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from LimitUploadSize import LimitUploadSize
from primeNumbers import *
from invertPhoto import *

app = FastAPI()

app.add_middleware(LimitUploadSize, max_upload_size=12_000_000)

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
    save_image(file, file.filename)
    move_image(file.filename)
    return {"name_of_file": file.filename}


@app.get("/picture/invert/{filename}")
async def display_photo(request: Request, filename: str = Path(
    description="The name of the file"
)):
    invert_photo_colors(filename)
    return StreamingResponse(display_image(filename), media_type="image/png")
