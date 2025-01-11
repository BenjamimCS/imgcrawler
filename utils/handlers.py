from .url import basename
from tqdm import tqdm
from typing import Callable
__all__ = ['makerequest', 'readfile']

def _reportget(response, filename:str): pass

def _reportsuccessreadfile(filename:str, mode:str='r'):
  import os
  if   'rw' in mode: pass
  elif 'r'  in mode: print(f'\033[32m=> \33[33m{os.path.basename(filename)}\33[32m fully loaded\033[0m')
  elif 'w'  in mode: pass

def _reportfailurereadfile(filename:str, errortype='default'):
  match errortype:
    case 'filenotfound': print(f'\33[31m=> \33[33m{filename}\33[31m: file not found\33[0m')
    case 'typeerror':    print(f'\33[31m=> \33[33m{filename}\33[31m: no function for reportmsg["success"]\33[0m')
    case _:              print(f'\33[31m=> \33[33m{filename}\33[31m: an error ocurred while reading/writing the file\33[0m')

_readfileoptions = {
  'failure': _reportfailurereadfile,
  'success': _reportsuccessreadfile
}

makerequestoptions = {
  'failure': {
  },
  'get': _reportget
}

def makerequest(*args,sources:tuple[str]|list[str]|str=(), output:str="", log:bool=True, **kwargs):
  """
  Requests's module wrapper. Handles possible exceptions
  :sources -> tuple[str] | list[str]: URLs for request
  :output -> str: directory to store donwloaded files
  :log -> bool: report download progress
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
  except requests.exceptions.ConnectTimeout as error:
    print(f'\33[31m=> The request timed out while trying to connect to the remote server\n\33[0m   {error}')
    exit(1)
  except requests.exceptions.ConnectionError as error:
    print(f'\33[31m=> A connection error ocurred\n\33[0m   {error}')
    exit(1)
  except requests.exceptions.HTTPError as error:
    print(f'\33[31m=> An HTTP error has ocurred\n\33[0m   {error}')
    exit(1)
  except requests.exceptions.Timeout as error:
    print(f'\33[31m=> The request timed out\n\33[0m   {error}')
    exit(1)
  except Exception as error:
    print(error)
    exit(2)

def readfile(*args,report:bool=False, reportmsg:dict[str, (dict[str, str], Callable)]=_readfileoptions, **kwargs):
  """
  open's functon wrapper. Handles possible exceptions
  :*args: positional arguments for `open`
  :**kwargs: optional arguments for `open`
  :report -> bool: enable logging
  :reportmsg -> dict: for custom logging message
    It stores two keys: 'success' and 'failure'
    'success' -> Callable: report success accordingly with the current operation (reading, writing etc.)
    'failure' -> [dict,str]:
      'default'
      'filenotfound'
      'default'
      'typeerror'
  """
  import io
  # reportmsg = {**readfileoptions, **reportmsg} a way to update readfileoptions' keys' values
  try:
    file =  open(*args,**kwargs)
    if report: reportmsg['success'](*args, **kwargs)
    return file
  except FileNotFoundError:
    if report: reportmsg['failure'](*args, errortype='filenotfound')
    return io.StringIO("{}")
  except OSError:
    if report: reportmsg['failure'](*args)
    exit(1)
  except TypeError:
    if report: reportmsg['failure'](*args, errortype='typeerror')
    exit(1)
  except Exception:
    if report: reportmsg['failure'](*args)
    exit(1)
