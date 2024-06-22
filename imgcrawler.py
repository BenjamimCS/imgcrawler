import os
import json
import requests
from bs4 import BeautifulSoup
from utils.char import *
from utils.url  import *
from utils.handlers import *

# Get URL from HTML files and save in txt files
# and let it up to shell
# Precedence order:
#   1. command-line
#   2. json file
# TODO:
#   * log to the user
#   * parameters:
#     -s or --skip (skip the prompts)
#     -w or --site (site url)
#     -u or --url  (URL to get)
#     -p or --path (path for the image)
config = {
  'local': False,
  'replace': [],
  'site': '',
  'local_file': '',
  'dirname': '',
  'query': 'img',
  'savedir':'',
}

with readfile('setup.json', mode='rb') as json_file:
  config = {**config,**json.load(json_file)}

site         = (input("Website: ")       or config['site']) # input("Website: ")
newdirname   = (input("Real URL: ")      or config['dirname'])
savedir      = (input("Save location: ") or config['savedir'])
selector     = (input("Query for (any CSS selector for an <img>): ") or config["query"])
replace      = config['replace']
local        = config['local']
local_file   = config['local_file']

if local:
  with readfile(config['local_file'], 'rb') as html:
    dom = BeautifulSoup(html, 'html.parser')
else:
  response     = makerequest(requests.get,site)
  html = response.text
  dom = BeautifulSoup(html, 'html.parser')

sources      = [] # store all the images sources

try:
  for element in dom.select(selector):
    # from docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#miscellaneous
    url = element.get('src')
    if not url: url = element.get('href')
    if not url: continue

    urltest = deletechar(r'(\?|#).*', url)
    # only the supported types by web browsers
    isimg = re.search(r'\.(a?png|p?j(fif|pe?g?)|webp|gif|bmp|svg|avif|tiff?|ico)$', urltest)
    if not isimg: continue
    sources.append(url)
except Exception:
  pass

def get():
  if not os.path.exists(savedir):
    os.makedirs(savedir, exist_ok=True)

  try:
    for url in sources:
      if replace:
        url = url.replace(replace[0], replace[1])

      if not isurl(url): url = makeurl(site=site,path=url) # if there's just the path part
      filename = basename(url)
      response = makerequest(requests.get, url)
      if not response: continue # TODO: report error
      with readfile(file=f"{savedir}/{filename}", mode='wb') as outputfile:
        outputfile.write(response.content)
  except KeyError: pass

get()

