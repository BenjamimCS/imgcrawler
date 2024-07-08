from tqdm import tqdm
from typing import Callable
__all__ = ['makerequest', 'readfile']

def _reportget(response, filename:str):
  total = int(response.headers.get('content-length'))
  chunck = 8192
  options = {
    'desc': filename,
    'total': total,
    'unit': 'B',
    'unit_scale': True,
    'unit_divisor': 1024,
    'position': 0,
    'bar_format': '{desc}: {percentage:3.0f}% {bar} {n_fmt}B/{total_fmt}B [{elapsed}, {rate_fmt}]',
    'leave': None
  }

  with tqdm(**options) as progressbar:
    for c in response.iter_content(chunck):
      progressbar.update(len(c))


readfileoptions = {
  'failure': {
    'filenotfound': '\033[31m=> File not found\033[0m',
    'default': '\033[31m=> Unhandled \033[34mOSError\033[0m',
    'typeerorr': '\033[31=> No function for reportmsg["success"]\033[0m'
  },
  'success': lambda: print('\033[32m=> File found]')
}

makerequestoptions = {
  'failure': {
  },
  'get': _reportget
}

def makerequest(func, *args, report=False, reportmsg:dict=makerequestoptions, filename:str="", **kwargs):
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

    if report and kwargs.get('stream'):
      response = func(*args, **kwargs)
      reportmsg['get'](response, (filename or args[0]))
    else: return func(*args, **kwargs)
  except requests.exceptions.ConnectTimeout: pass
  except requests.exceptions.ConnectionError: pass
  except requests.exceptions.HTTPError: pass
  except requests.exceptions.Timeout: pass
  except Exception: pass

def readfile(*args,report:bool=False, reportmsg:dict[str, (dict[str, str], Callable)]=readfileoptions, **kwargs):
  """
  open's functon wrapper. Handles possible exceptions
  :*args: positional arguments
  :*report* -> bool: enable logging
  :*reportmsg* -> dict: for custom logging message
    It stores two keys: 'success' and 'failure'
    'success' -> Callable: report success accordingly with the current operation (reading, writing etc.)
    'failure' -> [dict,str]:
      'filenotfound'
      'default'
  :**kwargs: keyowrd arguments
  """
  import io
  # reportmsg = {**readfileoptions, **reportmsg} a way to update readfileoptions' keys' values
  try:
    file =  open(*args,**kwargs)
    if report: reportmsg['success']()
    return file
  except FileNotFoundError:
    if report: print(reportmsg['failure']['filenotfound'])
    return io.StringIO("{}")
  except OSError:
    if report: print(reportmsg['failure']['default'])
    exit(1)
  except TypeError:
    if report: print(reportmsg['failure']['typeerror'])
    exit(1)
  except Exception:
    print(reportmsg['failure']['default'])
    exit(1)
