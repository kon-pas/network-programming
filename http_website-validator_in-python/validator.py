import requests, sys
from bs4 import BeautifulSoup

URL = 'http://th.if.uj.edu.pl/'
ELEMENT = {'tag': 'meta', 'attributes': {'name': 'author', 'content': 'Przemek Witaszczyk 2015'}}

def validate(url, element = {}):
  """
  Function validating if a website is working as intended.

  @param {string} url - Website's URL address.
  @param {Dictionary} [element={}] - Element which the website has to contain, as follows:
    {string} tag - Name of element's tag type.
    {Dictionary} attributes - Contains all pairs attribute-value which the element has to contain, following HTML specification.
  
  @returns {integer} System status code, as follows:
    0 : SUCCESS
    1 : HTTP STATUS RESPONSE CODE NOT 200
    2 : CONTENT TYPE NOT TEXT/HTML
    3 : CONTENT NOT DESIRED WEBSITE
  """
  with requests.get(url) as response:
    if response.status_code == 200:
      if "text/html" in response.headers.get("Content-Type"):
        website = BeautifulSoup(response.content, 'html.parser')
        if element:
          if website.find(element['tag'], element['attributes']): sys.exit(0)
          else: sys.exit(3)
        else: sys.exit(0)
      else: sys.exit(2)
    else: sys.exit(1)

if __name__ == "__main__":
  validate(URL, ELEMENT)