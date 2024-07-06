import re
__all__ = ['match']

def match(pattern:str, string:str) -> str | None:
  """
  Returns the matched string, None otherwise
  """
  if not pattern: return None

  matches = re.search(pattern, string)
  if matches: return string[matches.start():matches.end()]
  else:       return None
