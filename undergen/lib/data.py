from undergen.lib.audio import get_sound as get_sound_ext
from undergen.lib.image import get_image as get_image_ext


class Character:
    def __init__(self, name: str, *, darkworld: bool = False, image_name: str = None, valid_expressions: list[str] = [], sound_name: str = None, font: str = None):
        self.name = name
        self.darkworld = darkworld
        self._image_name = image_name
        self.valid_expressions = valid_expressions
        self._sound_name = sound_name
        self._font = font

    @property
    def image_name(self):
        return self._image_name if self._image_name is not None else self.name

    @property
    def sound_name(self):
        return self._sound_name if self._sound_name is not None else self.name.title()

    @property
    def font(self):
        return self._font if self._font is not None else "determination"

    def get_image(self, expression: str, text: str, animated: bool = True):
        if self.valid_expressions:
            if expression not in self.valid_expressions:
                raise ValueError(f"Expression {expression} not a valid expression for character {self.name}.")
        return get_image_ext(self, expression, text, animated = animated)

    def get_sound(self, text: str):
        return get_sound_ext(self, text)

    def get_image_and_sound(self, expression: str, text: str, animated: bool = True):
        return self.get_image(expression, text, animated), self.get_sound(text)

    def to_json(self):
        return {
            "name": self.name,
            "darkworld": self.darkworld,
            "image_name": self._image_name,
            "valid_expressions": self.valid_expressions,
            "sound_name": self._sound_name,
            "font": self.font
        }

    @classmethod
    def from_json(cls, jsondata: dict) -> "Character":
        name = jsondata["name"]
        darkworld = jsondata.get("darkworld")
        image_name = jsondata.get("image_name")
        valid_expressions = jsondata.get("valid_expressions")
        sound_name = jsondata.get("sound_name")
        font = jsondata.get("font")
        return Character(name, darkworld = darkworld, image_name = image_name, valid_expressions = valid_expressions, sound_name = sound_name, font = font)


class CharacterDB:
    def __init__(self, characters: list[Character]):
        self._characters = characters

    @property
    def names(self):
        return [c.name for c in self._characters]

    def get(self, name: str):
        try:
            return next(c for c in self._characters if c.name == name)
        except StopIteration:
            raise ValueError(f"No such character '{name}'.")

    def add(self, character: Character):
        if character.name in self.names:
            raise ValueError(f"'{character.name}' already registered.")
        self._characters.append(character)

    def remove(self, name: str):
        self._characters = [c for c in self._characters if c.name != name]

    def to_json(self):
        return [c.to_json() for c in self._characters]

    @classmethod
    def from_json(cls, jsondata):
        return CharacterDB([Character.from_json(c) for c in jsondata])
