from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from undergen.lib.data import Character

url_template = "https://www.demirramon.com/gen/undertale_text_box.{format}?text={text}&box={box}&boxcolor=ffffff&character={character}&expression={expression}&font={font}&asterisk=ffffff&mode={mode}&animate={animate}"


def get_image(character: "Character", expression: str, text: str, animated: bool = True):
    params = {}

    # Validation
    if character.valid_expressions:
        if expression not in character.valid_expressions:
            raise ValueError(f"'{expression}' not a valid expresion for {character.name}.")

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

    return response.content
