import re
import logging

def extractMovieScenes(movieScript):
    logging.debug("#####################################################")
    logging.debug("####")
    logging.debug("#### Establishing interactions between characters")
    logging.debug("####")
    logging.debug("#####################################################")

    p = re.compile(ur'(<pre>BLACK SCREEN|<b>EXT\.|<b>INT\.)(?P<movie_text>.*?)(?=<b>(EXT\.|INT\.))', re.MULTILINE | re.DOTALL)
    text = []

    for m in re.finditer(ur'(<pre>BLACK SCREEN|<b>EXT\.|<b>INT\.)(?P<movie_text>.*?)(?=<b>(EXT\.|INT\.))', movieScript):
        text.append(m.group("movie_text"))
     
    return text
