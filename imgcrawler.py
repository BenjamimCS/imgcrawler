import os,json,requests
from bs4 import BeautifulSoup

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
  'query': '',
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

for element in dom.select(selector):
  sources.append(element['src'])

def get():
  if not os.path.exists(savedir):
    os.makedirs(savedir, exist_ok=True)

  for file in sources:
    if replace:
      try:
        for s in replace:
          file = file.replace(s[0], s[1])
      except KeyError:
        pass # implement error
    basename = os.path.basename(file)
    response = requests.get(file)
    o        = open(file=f"{savedir}/{basename}", mode='wb')
    o.write(response.content)
get()

