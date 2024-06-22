import re

urlschemeregex = r'(\w+)'
urlpathregex = r'(\/.*)?'
urlauthorityregex = r'\/\/((?:[a-z0-9%]+\.)?[a-z0-9%]+(?:\.[a-z]+)+)' # before path of scheme-specific-part
urlregex = urlschemeregex + ':' + urlauthorityregex + urlpathregex

def isurl(url:str) -> bool:
  matches = re.fullmatch(urlregex, url)
  if matches: return True
  else:       return False

def gethost(url:str) -> str:
  if not isurl(url): raise ValueError('*url* is not a valid URL')

  host = re.search(urlauthorityregex, url, re.IGNORECASE)
  return host.group(1)

def getprotocol(url:str) -> str:
  protocol = re.match(urlschemeregex, url, re.IGNORECASE)
  return protocol.group(1)

def makeurl(site:str, path:str, protocol:str = 'https'):
  pattern = re.search(urlpathregex, site)

  if pattern:
    host = gethost(site)
    return f"{protocol}://{host}{path}"

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
  from . import char
  if not isurl(url): return url
  urlbasename = os.path.basename(url)
  urlbasename = char.deletechar(r'(\?|#).*', urlbasename)
  if not urlbasename: pass # TODO: if empty return a random string with # at the beginning
  return urlbasename
