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

def readfile(*args,**kwargs):
  """
  open's functon wrapper. Handles possible exceptions
  :*args: positional arguments
  :**kwargs: keyowrd arguments
  """
  try:
    return open(*args,**kwargs)
  except FileNotFoundError:
    pass
    exit(1)
  except Exception as err:
    pass
    exit(1)
