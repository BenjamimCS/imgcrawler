import os
import json
import requests
from bs4 import BeautifulSoup
from utils.char import *
from utils.url  import *

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

try:
  settingsjson = json.load(open('setup.json'))
  for i in settingsjson:
    config[i] = settingsjson[i]
  del settingsjson
except FileNotFoundError:
  pass

site         = (input("Website: ")       or config['site']) # input("Website: ")
newdirname   = (input("Real URL: ")      or config['dirname'])
savedir      = (input("Save location: ") or config['savedir'])
selector     = (input("Query for (any CSS selector for an <img>): ") or config["query"])
replace      = config['replace']
local        = config['local']
local_file   = config['local_file']

if local:
  html = open(config['local_file'], 'rb')
else:
  response     = requests.get(site)
  html = response.text

dom         = BeautifulSoup(html, 'html.parser')
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

  for url in sources:
    if replace:
        url = url.replace(replace[0], replace[1])

    if not isurl(url): url = makeurl(site=site,path=url) # if there's just the path part
    basename = os.path.basename(url)
    basename = deletechar(r'\?.*',basename) or basename # remove any leading query string
    response = requests.get(url)
    o        = open(file=f"{savedir}/{basename}", mode='wb')
    o.write(response.content)

get()

