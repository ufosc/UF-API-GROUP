from fastapi import FastAPI, UploadFile, Response, APIRouter
from PIL import Image
import uvicorn
import io


if __name__ == "__main__":
    app = FastAPI()
else:
    app = APIRouter()


# Prompts the user to select their image file
@app.post(
    "/rotate-image",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def create_upload_file(file: UploadFile):
    # error handling if nothing uploaded
    if file.filename == "":
        return {"error": "No file selected"}

    # error handling if file is not image
    if file.content_type.startswith("image/") is False:
        return {"error": "File is not an image"}

    # create a holder to store image
    new_image = io.BytesIO()

    # rotate image 90 degrees
    Image.open(file.file).rotate(90, expand=True).save(
        new_image, format=file.content_type[6:], optimize=True
    )
    new_image.seek(0)

    # return image
    return Response(content=new_image.read(), media_type=file.content_type)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
