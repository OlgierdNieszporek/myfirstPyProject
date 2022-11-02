from fastapi import FastAPI, Path, UploadFile, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from starlette.requests import Request
from starlette.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from LimitUploadSize import LimitUploadSize
from authenthication import get_time
from primeNumbers import *
from invertPhoto import *

app = FastAPI()

app.add_middleware(LimitUploadSize, max_upload_size=12_000_000)

templates = Jinja2Templates(directory="templates")

app.mount("/images", StaticFiles(directory="images"), name="images")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    return {"access_token": form_data.username, "token_type": "bearer"}


@app.get("/authorized-users/time")
async def authenticate(token: str = Depends(oauth_scheme)):
    print(token)
    return {get_time()}
