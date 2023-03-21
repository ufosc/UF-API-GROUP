from fastapi import FastAPI, UploadFile, Response
from PIL import Image
import uvicorn

app = FastAPI()


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

    # rotate image 90 degrees
    Image.open(file.file).rotate(90).save(file.filename)

    # return image
    image_bytes = open(file.filename, "rb").read()
    return Response(content=image_bytes, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
