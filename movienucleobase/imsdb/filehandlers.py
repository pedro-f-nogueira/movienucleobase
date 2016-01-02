"""
.. module:: filehandlers
    :synopsis: A module to handle the HTML files from IMSDb

.. moduleauthor:: Pedro Araujo <pedroaraujo@colorlesscube.com>
.. moduleauthor:: Pedro Nogueira <pedro.fig.nogueira@gmail.com>
"""

import logging


def open_movie_script(filename):
    """Receives the name of a HTML file and returns the contents as a list.
    
    The function attempts to remove the HTML header that comes before the
    movie script in order to avoid any unexpected behavior from the HTML tags.

    Args:
        filename (string): The name of the HTML file

    Returns:
        list of strings: Contains the contents of the HTML minus the header.

    Raises:
        It raises an exception if the file cannot be found.
    """

    logger = logging.getLogger(__name__)

    try:
        with open(filename, 'r') as html_file:
            # Remove all new lines char, we don't need them since each line
            # will represent a new index in the list
            imsdb_movie_script = html_file.read().replace('\n', '')

            # In the HTML page, everything that comes before the
            # following HTML code is consider an header and useless
            # for the movie info extraction
            # TODO: This HTML line is hardcoded in the code, it could be
            # somehow parameterized
            html_code = '<br> <table width=\"100%\">'

            if html_code not in imsdb_movie_script:
                print "Error: Unable to split file by the following string:" + \
                        html_code
                return

            imsdb_movie_script = imsdb_movie_script.split(html_code)[1]

            logger.info('File successfully opened: ' + filename)

            return imsdb_movie_script
    except:
        raise


