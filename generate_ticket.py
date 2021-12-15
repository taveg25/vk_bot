#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = "files/ticket_billet.jpg"
FONT_PATH = "files/Roboto-Regular.ttf"
FONT_SIZE = 25

BLACK = (0, 0, 0, 255)
NAME_OFFSET = (240, 200)
EMAIL_OFFSET = (240, 235)

AVATAR_SIZE = 100
AVATAR_OFFSET = (65, 190)

def generate_ticket(name, email):
    with Image.open(TEMPLATE_PATH).convert("RGBA") as base:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        draw = ImageDraw.Draw(base)
        draw.text(NAME_OFFSET, name, font=font, fill=BLACK)
        draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK)

        response = requests.get(url=f'https://avatars.dicebear.com/api/identicon/{email}.png?size={AVATAR_SIZE}')
        avatar_file_like = BytesIO(response.content)

        avatar = Image.open(avatar_file_like)

        base.paste(avatar, AVATAR_OFFSET)

        temp_file = BytesIO()
        base.save(temp_file, 'png')
        temp_file.seek(0)

        return temp_file
