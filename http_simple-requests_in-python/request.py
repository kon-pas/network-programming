import sys
import requests
import xmltodict

"""Discogs

page_number = 1
while True:
  with requests.get(f"https://api.discogs.com/artists/45467/releases?page={page_number}&per_page=100") as response:
    if response.status_code == 200:
      if "application/json" in response.headers.get("Content-Type"):
        if releases := response.json()['releases']:
          for idx, release in enumerate(releases):
            print(release['title'])
        else: sys.exit(3)
      else: sys.exit(2)
    else: sys.exit(1)
  page_number += 1
"""

"""Music Brainz

with requests.get("https://musicbrainz.org/ws/2/release-group?artist=5441c29d-3602-4898-b1a1-b77fa23b8e50&type=album|ep") as response:
  if response.status_code == 200:
    if "application/xml" in response.headers.get("Content-Type"):
      if dictionary := xmltodict.parse(response.content):
        for album in dictionary['metadata']['release-group-list']['release-group']:
          print(album['title'])
      else: sys.exit(3)
    else: sys.exit(2)
  else: sys.exit(1)
"""