import os
import random
import re
import textwrap
import numpy as np
import aiofiles
import aiohttp
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch
from RiruruMusic import app, LOGGER
from config import YOUTUBE_IMG_URL
from RiruruMusic.assets import bgs


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def add_corners(im):
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, im.split()[-1])
    im.putalpha(mask)


async def gen_thumb(videoid, user_id):
    fuck = random.choice(bgs)
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                result["viewCount"]["short"]
            except:
                pass
            try:
                result["channel"]["name"]
            except:
                pass

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()
        lucky = await app.get_profile_photos(user_id)
        try:
            hmm = await app.download_media(lucky[0]['file_id'], file_name=f'{user_id}.jpg')
        except Exception as e:
            LOGGER("RiruruMusic").error(e)
            umm = await app.get_profile_photos(app.id)
            hmm = await app.download_media(umm[0]['file_id'], file_name=f'{app.id}.jpg')
        op = Image.open(hmm)
        a = Image.new('L', [640, 640], 0)
        b = ImageDraw.Draw(a)
        b.pieslice([(0, 0), (640,640)], 0, 360, fill = 255, outline = "grey")
        c = np.array(op)
        d = np.array(a)
        e = np.dstack((c, d))
        f = Image.fromarray(e)
        x = f.resize((145, 145))

        youtube = Image.open(f"cache/thumb{videoid}.png")
        bg = Image.open(f"RiruruMusic/assets/{fuck}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        image2 = background

        image3 = changeImageSize(1280, 720, bg)
        image5 = image3.convert("RGBA")
        image2.paste(x, (65, 32), mask = x)
        image2.paste(x, (1065, 32), mask = x)
        image2.paste(x, (1060, 530), mask = x)
        image2.paste(x, (65, 530), mask = x)
        Image.alpha_composite(background, image5).save(f"cache/temp{videoid}.png")

        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = youtube.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
        logo.save(f"cache/chop{videoid}.png")
        if not os.path.isfile(f"cache/cropped{videoid}.png"):
            im = Image.open(f"cache/chop{videoid}.png").convert("RGBA")
            add_corners(im)
            im.save(f"cache/cropped{videoid}.png")

        crop_img = Image.open(f"cache/cropped{videoid}.png")
        logo = crop_img.convert("RGBA")
        logo.thumbnail((365, 365), Image.ANTIALIAS)
        width = int((1280 - 365) / 2)
        background = Image.open(f"cache/temp{videoid}.png")
        background.paste(logo, (width + 2, 134), mask=logo)

        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("RiruruMusic/assets/font2.ttf", 45)
        ImageFont.truetype("RiruruMusic/assets/font2.ttf", 70)
        arial = ImageFont.truetype("RiruruMusic/assets/font2.ttf", 30)
        ImageFont.truetype("RiruruMusic/assets/font.ttf", 30)
        para = textwrap.wrap(title, width=32)
        try:
            draw.text(
                (450, 25),
                f"STARTED PLAYING",
                fill="white",
                stroke_width=2,
                stroke_fill="pink",
                font=font,
            )
            if para[0]:
                text_w, text_h = draw.textsize(f"{para[0]}", font=font)
                draw.text(
                    ((1280 - text_w) / 2, 550),
                    f"{para[0]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="pink",
                    font=font,
                )
            if para[1]:
                text_w, text_h = draw.textsize(f"{para[1]}", font=font)
                draw.text(
                    ((1280 - text_w) / 2, 600),
                    f"{para[1]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="pink",
                    font=font,
                )
        except:
            pass
        text_w, text_h = draw.textsize(f"Duration: {duration} Mins", font=arial)
        draw.text(
            ((1280 - text_w) / 2, 660),
            f"Duration: {duration} Mins",
            fill="white",
            font=arial,
        )

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}_{fuck}.png")
        return f"cache/{videoid}_{fuck}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL


async def gen_qthumb(videoid, user_id):
    fuck = random.choice(bgs)
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                result["viewCount"]["short"]
            except:
                pass
            try:
                result["channel"]["name"]
            except:
                pass

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()
        lucky = await app.get_profile_photos(user_id)
        try:
            hmm = await app.download_media(lucky[0]['file_id'], file_name=f'{user_id}.jpg')
        except Exception as e:
            LOGGER("RiruruMusic").error(e)
            umm = await app.get_profile_photos(app.id)
            hmm = await app.download_media(umm[0]['file_id'], file_name=f'{app.id}.jpg')
        op = Image.open(hmm)
        a = Image.new('L', [640, 640], 0)
        b = ImageDraw.Draw(a)
        b.pieslice([(0, 0), (640,640)], 0, 360, fill = 255, outline = "grey")
        c = np.array(op)
        d = np.array(a)
        e = np.dstack((c, d))
        f = Image.fromarray(e)
        x = f.resize((145, 145))

        youtube = Image.open(f"cache/thumb{videoid}.png")
        bg = Image.open(f"RiruruMusic/assets/{fuck}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        image2 = background

        image3 = changeImageSize(1280, 720, bg)
        image5 = image3.convert("RGBA")
        image2.paste(x, (65, 32), mask = x)
        image2.paste(x, (1065, 32), mask = x)
        image2.paste(x, (1060, 530), mask = x)
        image2.paste(x, (65, 530), mask = x)
        Image.alpha_composite(background, image5).save(f"cache/temp{videoid}.png")

        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = youtube.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
        logo.save(f"cache/chop{videoid}.png")
        if not os.path.isfile(f"cache/cropped{videoid}.png"):
            im = Image.open(f"cache/chop{videoid}.png").convert("RGBA")
            add_corners(im)
            im.save(f"cache/cropped{videoid}.png")

        crop_img = Image.open(f"cache/cropped{videoid}.png")
        logo = crop_img.convert("RGBA")
        logo.thumbnail((365, 365), Image.ANTIALIAS)
        width = int((1280 - 365) / 2)
        background = Image.open(f"cache/temp{videoid}.png")
        background.paste(logo, (width + 2, 134), mask=logo)

        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("RiruruMusic/assets/font2.ttf", 45)
        ImageFont.truetype("RiruruMusic/assets/font2.ttf", 70)
        arial = ImageFont.truetype("RiruruMusic/assets/font2.ttf", 30)
        ImageFont.truetype("RiruruMusic/assets/font.ttf", 30)
        para = textwrap.wrap(title, width=32)
        try:
            draw.text(
                (455, 25),
                "ADDED TO QUEUE",
                fill="white",
                stroke_width=2,
                stroke_fill="pink",
                font=font,
            )
            if para[0]:
                text_w, text_h = draw.textsize(f"{para[0]}", font=font)
                draw.text(
                    ((1280 - text_w) / 2, 550),
                    f"{para[0]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="pink",
                    font=font,
                )
            if para[1]:
                text_w, text_h = draw.textsize(f"{para[1]}", font=font)
                draw.text(
                    ((1280 - text_w) / 2, 600),
                    f"{para[1]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="pink",
                    font=font,
                )
        except:
            pass
        text_w, text_h = draw.textsize(f"Duration: {duration} Mins", font=arial)
        draw.text(
            ((1280 - text_w) / 2, 660),
            f"Duration: {duration} Mins",
            fill="white",
            font=arial,
        )

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/que{videoid}_{fuck}.png")
        return f"cache/que{videoid}_{fuck}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
