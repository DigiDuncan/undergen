import time

from undergen.lib.data import Character, CharacterDB

db = CharacterDB([
    Character("ralsei", darkworld = True),
    Character("sans")
])


def main():
    name = str(round(time.time()))
    ralsei = db.get("ralsei")
    image, sound = ralsei.get_image_and_sound("smile-blush", "Thank you for making me your test!")
    with open(f"./test_images/{name}.gif", "wb") as f:
        f.write(image)
    with open(f"./test_images/{name}.wav", "wb") as f:
        f.write(sound)


if __name__ == "__main__":
    main()
