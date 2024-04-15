import re

urlregex = r'(https?):\/\/((?:[a-z1-9%]+\.)?[a-z1-9%]+(?:\.[a-z]+)+)'
urlpathregex = urlregex + r'(\/.*)?'

def isurl(url:str) -> bool:
  matches = re.fullmatch(urlpathregex, url)
  if matches: return True
  else:       return False

def gethost(url:str) -> str:
  if not isurl(url): raise ValueError('*url* is not a valid URL')

  host = re.search(urlregex, url, re.IGNORECASE)
  return host.group(2)

def getprotocol(url:str) -> str:
  protocol = re.match(urlregex, url, re.IGNORECASE)
  return protocol.group(2)

def makeurl(site:str='', path:str = '', protocol:str = 'https'):
  pattern = re.search(urlpathregex, site)

  if pattern:
    host = gethost(site)
    return f"{protocol}://{host}{path}"

def isroot(url:str) -> bool:
  if re.match('/', url): return True
  else: return False
