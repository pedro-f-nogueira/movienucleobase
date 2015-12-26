import re

def extractMovieScenes(movieScript):
    p = re.compile(ur'(<pre>BLACK SCREEN|<b>EXT\.|<b>INT\.)(?P<movie_text>.*?)(?=<b>(EXT\.|INT\.))', re.MULTILINE | re.DOTALL)
    text = []

    for m in re.finditer(ur'(<pre>BLACK SCREEN|<b>EXT\.|<b>INT\.)(?P<movie_text>.*?)(?=<b>(EXT\.|INT\.))', movieScript):
        text.append(m.group("movie_text"))
     
    return text
