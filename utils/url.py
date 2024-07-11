import re

__all__ = [  'isurl',  'gethost', 'getprotocol',
           'makeurl',  'isroot' ,    'basename']

URLSCHEMEREGEX = r'^(\w+)'
URLPATHREGEX = r'(\/.*)?'
URLAUTHORITYREGEX = r'((?:[a-z0-9%-_]+\.)?[a-z0-9%_-]+(?:\.[a-z]+)+)' # before path of scheme-specific-part
URLREGEX = URLSCHEMEREGEX + '://' + URLAUTHORITYREGEX + URLPATHREGEX

def isurl(url:str) -> bool:
  matches = re.fullmatch(URLREGEX, url)
  if matches: return True
  else:       return False

def gethost(url:str) -> str:
  if not isurl(url): raise ValueError('*url* is not a valid URL')

  host = re.search(URLAUTHORITYREGEX, url, re.IGNORECASE)
  return host.group(1)

def getprotocol(url:str) -> str:
  protocol = re.match(URLSCHEMEREGEX, url, re.IGNORECASE)
  return protocol.group(1)

def makeurl(baseurl:str, path:str, protocol:str = 'https') -> str | None:
  """
  Produce an URL with *path* if *baseurl* exits. Return None instead
  :baseurl -> str: the reference URL
  :path -> str: the path to be transformed
  :protocol -> str: an optional protocol for the final URL
  """
  import os
  if not isurl(baseurl): return path
  QUERYSTRINGPATTERN = re.compile(r'(\?.+)')

  host = os.path.dirname(baseurl)
  if QUERYSTRINGPATTERN.search(baseurl):
    querystring = QUERYSTRINGPATTERN.search(baseurl).group(1)
  else: querystring = ''

  if protocol:
    baseurl = re.sub(r'^\w+:', f'{protocol}:', baseurl)
  host = os.path.dirname(baseurl)
  if re.search(r'^\./', path):
    path = re.sub(r'^\./', '/', path)
    return f"{host}{path}{querystring}"
  elif re.search(r'^/', path):
    return f"{host}{path}{querystring}"
  else:
    return f'{host}/{path}{querystring}'

def isroot(url:str) -> bool:
  if re.match('/', url): return True
  else: return False

def basename(url:str) -> str:
  """
  Get the basename from an URL
  If  :url: isn't a valid URL its value is returned
  :url -> str: a valid URL
  """
  import os
  if not isurl(url): return url
  urlbasename = os.path.basename(url)
  urlbasename = re.sub(r'(\?|#).*', '', urlbasename)
  if not urlbasename: pass # TODO: if empty return a random string with # at the beginning
  return urlbasename
