# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector for exashare.com
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# by DrZ3r0
# ------------------------------------------------------------

import re

from core import logger, httptools
from core import scrapertools


def test_video_exists(page_url):
    logger.info("[exashare.py] test_video_exists(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data

    if re.search("""File Not Found""", data):
        return False, 'Video non trovato'

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[exashare.py] url=" + page_url)
    video_urls = []

    data = httptools.downloadpage(page_url).data

    try:
        page_url = re.search('src="([^"]+)', data).group(1)
    except:
        return video_urls

    data = httptools.downloadpage(page_url).data

    # URL del vídeo
    url = re.search('file\s*:\s*"(http.+?)"', data)
    if url:
        url = url.group(1)
        video_urls.append([scrapertools.get_filename_from_url(url)[-4:] + " [exashare]", url])

    return video_urls  # Encuentra vídeos del servidor en el texto pasado


def find_videos(text):
    encontrados = set()
    devuelve = []

    patronvideos = r'//(?:www\.)?exashare\.com/(?:embed-)?(?!make)(?!image)(?!login)(?!contact)(?!player)([0-9A-Za-z]+)(?:\-[0-9]+x[0-9]+\.html)?'
    logger.info("[exashare.py] find_videos #" + patronvideos + "#")

    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for media_id in matches:
        titulo = "[exashare]"
        url = 'http://exashare.com/embed-%s.html' % media_id
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'exashare'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
