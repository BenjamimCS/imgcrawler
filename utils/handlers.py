from .url import basename
from tqdm import tqdm
from typing import Callable
__all__ = ['makerequest', 'readfile']

def _reportget(response, filename:str): pass


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

def makerequest(*args,sources:tuple[str]|list[str]|str=(), output:str="", log:bool=True, **kwargs):
  """
  Requests's module wrapper. Handles possible exceptions
  :sources -> tuple[str] | list[str]:
  :output -> str:
  :log -> str:
  """
  import requests
  try:
    if not output:
      response = requests.get(*args, **kwargs)
      response.raise_for_status()
      return response
    if log:
      options = {
        'unit': 'B',
        'unit_scale': True,
        'unit_divisor': 1024,
        'position': 0,
        'bar_format': '{desc}: {percentage:3.0f}% {bar} {n_fmt}B/{total_fmt}B [{elapsed}, {rate_fmt}]',
        'ncols': 100,
        'leave': None
      }
      for url in sources:
        filebasename = basename(url)
        options['desc'] = filebasename
        response = requests.get(url, stream=log)
        response.raise_for_status()
        options['total'] = int(response.headers.get('content-length'))
        chunk = 8192

        with tqdm(**options) as progressbar:
          for c in response.iter_content(chunk):
            progressbar.update(len(c))
            with open(f'{output}/{filebasename}', "ab+") as file:
              file.write(c)
    else:
      for url in sources:
        filebasename = basename(url)
        response = requests.get(url, stream=log)
        with open(f'{output}/{filebasename}', "ab+") as file:
          file.write(response.content)
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
