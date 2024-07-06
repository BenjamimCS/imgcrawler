__all__ = ['makerequest', 'readfile']

def makerequest(func, *args, **kwargs):
  """
  Requests's module wrapper. Handles possible exceptions
  :func -> function:
  :*args: positional arguments
  :**kwargs: keyowrd arguments
  """
  import requests
  try:
    # TODO: raise exception if *func* isn't member of requets module
    if not func in requests.__dict__: pass

    return func(*args, **kwargs)
  except requests.exceptions.ConnectTimeout: pass
  except requests.exceptions.ConnectionError: pass
  except requests.exceptions.HTTPError: pass
  except requests.exceptions.Timeout: pass
  except Exception: pass

def readfile(*args,report:bool=False, reportmsg={'failure': "file not found"}, **kwargs):
  """
  open's functon wrapper. Handles possible exceptions
  :*args: positional arguments
  :*report* -> bool: enable logging
  :*reportmsg* -> str: custom logging message
  :**kwargs: keyowrd arguments
  """
  import io
  try:
    return open(*args,**kwargs)
  except FileNotFoundError:
    if report: print(reportmsg['failure'])
    return io.StringIO("{}")
  except Exception as err:
    pass
    exit(1)
