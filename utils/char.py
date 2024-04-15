import re

def match(pattern:str, string:str) -> str | None:
  """
  Returns the matched string, None otherwise
  """
  if not pattern: return None

  matches = re.search(pattern, string)
  if matches: return string[matches.start():matches.end()]
  else:       return None

def deletechar(pattern: str, string: str) -> str:
  """
  Remove a *patern* from *string*
  """
  todel = match(pattern, string)
  if todel:
    return string.replace(todel, '')
  else: return string
