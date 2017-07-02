# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector for ok.ru
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# by DrZ3r0
# ------------------------------------------------------------

import re
import urllib

from core import httptools
from core import logger

headers = [
    ['User-Agent',
     'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'],
]


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    
    data = httptools.downloadpage(page_url).data
    if "copyrightsRestricted" in data or "COPYRIGHTS_RESTRICTED" in data:
        return False, "[Okru] Il file è stato rimosso per violazione del copyright"
    elif "notFound" in data:
        return False, "[Okru] Il file non esiste o è stato rimosso"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[okru.py] url=" + page_url)
    video_urls = []

    page_url = page_url.split('|')
    headers.append(['Referer', page_url[1]])

    page_url[0] = page_url[0].split('?')
    data = httptools.downloadpage(page_url[0][0], post=page_url[0][1], headers=headers).data

    _headers = urllib.urlencode(dict(headers))

    # URL del vídeo
    for vtype, url in re.findall(r'\{"name":"([^"]+)","url":"([^"]+)"', data, re.DOTALL):
        url = url.replace("%3B", ";").replace(r"\u0026", "&")
        url += '|' + _headers
        video_urls.append([vtype + " [okru]", url])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    patronvideos = '//(?:www.)?ok.../(?:videoembed|video)/(\d+)'
    logger.info("#" + patronvideos + "#")

    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for media_id in matches:
        titulo = "[okru]"
        url = 'http://ok.ru/dk?cmd=videoPlayerMetadata&mid=%s|http://ok.ru/videoembed/%s' % (media_id, media_id)
        if url not in encontrados:
            logger.info("url=" + url)
            devuelve.append([titulo, url, 'okru'])
            encontrados.add(url)
        else:
            logger.info("url duplicada=" + url)

    return devuelve
