from urllib.parse import unquote
import re

def _match(url, expression):
    match = re.match(expression, url)
    return match.groupdict()['item'] if match is not None else None

def match_protocol(url):
    return _match(url, r"^((?P<item>.+?)://)?")

def match_host(url):
    return _match(url, r"^.+?://((?P<item>.+?)($|[:/?#]))?")

def match_port(url):
    p = _match(url, r"^.+?://.+?:(?P<item>\d+)($|[/?#])")
    return int(p) if p else 80

def match_path(url):
    return _match(url, r"^.+?://.+?(?P<item>/.*?)($|[?#])")

def match_query(url):
    query_content = _match(url, r"^.+?://.+?[?](?P<item>.+?)($)")
    if query_content:
        return dict([i.split("=") for i in query_content.split('&')])
    else:
        return None

def match_fragment(url):
    return _match(url, r"^.+?://.+?[#](?P<item>.+?)($|[?])")

def has_valid_url_structure(url):
    return set(url) & set('.:/')

class ParsedURL(object):
    '''
    value object to store results of url parsing
    '''
    def __init__(self, url):
        url = unquote(url)

        if (not has_valid_url_structure(url)):
            raise ValueError('Invalid URL')

        self.url = url
        self.protocol = match_protocol(url)
        self.host = match_host(url)
        self.port = match_port(url)
        self.path = match_path(url)
        self.query = match_query(url)
        self.fragment = match_fragment(url)