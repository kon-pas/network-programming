#!/usr/bin/env python


'''
@author:  Konrad Pasternak
@date:    26/05/2022
'''


import sys
import os
import requests
import time
import json
from dataclasses import dataclass, field


DISCOGS_ULR_PREFIX          = "https://api.discogs.com"
FETCH_INTERVAL              = 2.5
DEFAULT_DESIGNATED_BAND_ID  = 94846


@dataclass
class Member:
  id    : int
  name  : str           = field(default='')
  bands : list['Band']  = field(default_factory=list)

  def add_band(self, band: 'Band') -> None:
    self.bands.append(band)


@dataclass
class Band:
  id      : int
  name    : str   = field(default='')
  members : list  = field(default_factory=list)

  def add_member(self, member: Member) -> None:
    if member not in self.members:
      self.members.append(member)


class WrongArgNum(Exception): pass


def handle_main(designated_band_id: int) -> None:
  with requests.get(f"{DISCOGS_ULR_PREFIX}/artists/{designated_band_id}") as response:
    if response.status_code == 200:
      if "application/json" in response.headers.get("Content-Type"):

        designated_band = json.loads(response.content)
        bands, members = [], []

        for member in designated_band["members"]:
          '''Initializes designated band members'''
          members.append(Member(member['id'], member['name']))

        for member in members:
          '''Initializes every band of every designated band member'''
          os.system('clear')
          print(f"May take some time, fetch interval set to {FETCH_INTERVAL} seconds due to server request rate limits", end="\n\n")
          print(f"Searching for band: {designated_band['name']}", end="\n\n")
          time.sleep(FETCH_INTERVAL)
          with requests.get(f"{DISCOGS_ULR_PREFIX}/artists/{member.id}") as response:
            if response.status_code == 200:
              if "application/json" in response.headers.get("Content-Type"):
                if groups := response.json()['groups']:
                  for group in groups:
                    band = next((band for band in bands if band.id == group['id']), None)
                    band.add_member(member) if band else bands.append(Band(group['id'], group['name'], [member]))
              else: sys.exit(2) # CONTENT TYPE NOT JSON
            else: sys.exit(1) # STATUS CODE NOT 200

        for band in sorted(bands, key=lambda band: band.name):
          '''Prints correlation in other bands between designated band members'''
          if len(band.members) > 1 and band.id != designated_band_id:
            print(f"{band.name} - {', '.join([member.name for member in band.members])}")

      else: sys.exit(2) # CONTENT TYPE NOT JSON
    else: sys.exit(1) # STATUS CODE NOT 200


if __name__ == '__main__':
  '''Fetches and prints correlation in other bands between designated band members
  
  :param arg1: Designated band ID
  :type arg1: int

  :return: Integer indicating fail status, as follows:
    0 : SUCCESS
    1 : STATUS CODE NOT 200
    2 : WRONG CONTENT TYPE
  :rtype: int
  '''
  match len(sys.argv) - 1:
    case 0:
      handle_main(DEFAULT_DESIGNATED_BAND_ID)
    case 1:
      handle_main(int(sys.argv[1]))
    case _:
      raise WrongArgNum("Too many arguments, provide only band's ID or leave empty for default ID")
  sys.exit(0)