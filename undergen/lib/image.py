import io
from typing import TYPE_CHECKING

import requests
from PIL import Image

if TYPE_CHECKING:
    from undergen.lib.data import Character

url_template = "https://www.demirramon.com/gen/undertale_text_box.{format}?text={text}&box={box}&boxcolor=ffffff&character={character}&expression={expression}&font={font}&asterisk=ffffff&mode={mode}&animate={animate}"


def get_image(character: "Character", expression: str, text: str, animated: bool = True):
    params = {}

    print(f"Getting image for {character.name}:{expression} '{text}'...")

    # Animated?
    if animated:
        params["format"] = "gif"
        params["animate"] = "true"
    else:
        params["format"] = "png"
        params["animate"] = "false"

    params["character"] = character.image_name
    params["mode"] = "regular" if not character.darkworld else "darkworld"
    params["box"] = "undertale" if not character.darkworld else "deltarune"
    params["font"] = character.font
    params["expression"] = expression
    params["text"] = text

    url = url_template.format_map(params)
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError(f"Box generator responded with code {response.status_code}.")

    print("Image success!")

    return params["format"], response.content


def merge_gifs(gifs: list[bytes], path: str, loop = False):
    loop_num = 0 if loop else 1
    print("Loading GIFs for merging...")
    gifs: list[Image.Image] = [Image.open(io.BytesIO(b)) for b in gifs]

    # Get durations
    durations = []
    for gif in gifs:
        if gif.is_animated:
            for i in range(0, gif.n_frames):
                gif.seek(i)
                durations.append(gif.info["duration"])
        else:
            raise ValueError("Got non-animated GIF!")

    print("Merge success!")
    image = gifs.pop(0)

    print("Writing merged GIF...")
    image.save(path, save_all = True, append_images = gifs, duration = durations, loop = loop_num)
