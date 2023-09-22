from fastapi import FastAPI, UploadFile, Response, APIRouter
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw
import uvicorn
import io


if __name__ == "__main__":
    app = FastAPI()
else:
    app = APIRouter()


# Medium Cut algorithm
def medium_cut_algorithm(colors, depth):
    palette = [[0, 0, 0]]
    palette_color = [0, 0, 0]
    if depth == 0 or len(colors) <= 1:
        for color in colors:
            for i in range(3):
                palette_color[i] += color[i]
        for i in range(3):
            palette_color[i] //= len(colors)
        return [palette_color]
    else:
        largest_red = 0
        smallest_red = 255
        largest_green = 0
        smallest_green = 255
        largest_blue = 0
        smallest_blue = 255

        for color in colors:
            if color[0] < smallest_red:
                smallest_red = color[0]

            if color[0] > largest_red:
                largest_red = color[0]

            if color[0] < smallest_green:
                smallest_green = color[1]

            if color[0] > largest_green:
                largest_green = color[1]

            if color[0] < smallest_blue:
                smallest_blue = color[2]

            if color[0] > largest_blue:
                largest_blue = color[2]

        red_diff = largest_red - smallest_red
        green_diff = largest_green - smallest_green
        blue_diff = largest_blue - smallest_blue

        if red_diff >= green_diff and red_diff >= blue_diff:
            colors.sort(key=lambda col: col[0])
        elif green_diff >= red_diff and green_diff >= blue_diff:
            colors.sort(key=lambda col: col[1])
        else:
            colors.sort(key=lambda col: col[2])

        palette_color = medium_cut_algorithm(colors[: len(colors) // 2], (depth - 1))
        palette = palette + palette_color
        palette.remove([0, 0, 0])
        palette_color = medium_cut_algorithm(colors[len(colors) // 2 :], (depth - 1))
        palette = palette + palette_color

    return palette


# Prompts the user to select their image file
@app.post(
    "/color-palette",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def grab_color_palette(file: UploadFile):
    # error handling if nothing uploaded
    if file.filename == "":
        return {"error": "No file selected"}

    # error handling if file is not image
    if file.content_type.startswith("image/") is False:
        return {"error": "File is not an image"}

    # get the colors of the file
    colors = list(Image.open(file.file).convert("RGB").getdata())

    # use the Median Cut algorithm to get a color palette
    palette = medium_cut_algorithm(colors, 4)  # Returns 2^depth colors

    # draw an image showing the pallete
    output = Image.new("RGB", (200, 200), (255, 255, 255, 0))
    x = 0
    y = 0
    d = ImageDraw.Draw(output)
    for i in palette:
        d.rectangle([x, y, x + 50, y + 50], tuple(i), None, 1)
        x += 50
        if x == 200:
            x = 0
            y += 50
    # creates a holder to store the image
    new_image = io.BytesIO()
    # saves output to it?
    output.save(new_image, format=file.content_type[6:], optimize=True)
    new_image.seek(0)

    # return color palette
    return StreamingResponse(content=new_image, media_type="image/jpeg")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
