import time

from undergen.lib.data import Character, CharacterDB
from undergen.lib.image import merge_gifs

db = CharacterDB([
    Character("ralsei", darkworld = True),
    Character("sans")
])


def test_single():
    name = str(round(time.time()))
    ralsei = db.get("ralsei")
    filetype, image, sound = ralsei.get_image_and_sound("smile-blush", "Thank you for making me your test!")
    print("Writing image...")
    with open(f"./test_images/{name}.{filetype}", "wb") as f:
        f.write(image)
    print("Writing audio...")
    with open(f"./test_images/{name}.wav", "wb") as f:
        f.write(sound)
    print("Done!")


def test_merge():
    name = str(round(time.time()))
    ralsei = db.get("ralsei")
    dialog = [
        ("smile-blush", "Thank you for making me your test!"),
        ("default", "I hope I'm doing this right.")
    ]
    images = []

    for d in dialog:
        images.append(ralsei.get_image(*d)[1])

    merge_gifs(images, f"./test_images/{name}.gif")


def main():
    pass


if __name__ == "__main__":
    main()
