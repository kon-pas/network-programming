#!/usr/bin/env python

"""
@author: Konrad Pasternak
@date: 18/05/2022
"""

import sys
import os

import requests
from bs4 import BeautifulSoup

RANKING_LENGTH = 15
RANKING_ITERATION_LIMIT = 40

SOCIAL_BLADE_SCRAP_LIMIT = 100
SOCIAL_BLADE_REAL_TIME_URL_PREFIX = "https://bastet.socialblade.com/twitter/lookup?query="
SOCIAL_BLADE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"

OKGREEN = "\033[92m"
FAIL = "\033[91m"
ENDC = "\033[0m"

class TwitterUser(object):
  def __init__(self, account_name: str, real_name: str) -> None:
    self._account_name = account_name[1:]
    self._real_name = real_name
    self._url = SOCIAL_BLADE_REAL_TIME_URL_PREFIX + self.account_name
    self._user_agent = SOCIAL_BLADE_USER_AGENT
    self._current = None
    self._prev = None
  
  @property
  def account_name(self) -> None: return self._account_name

  @property
  def real_name(self) -> None: return self._real_name

  @property
  def url(self) -> None: return self._url

  @property
  def user_agent(self) -> None: return self._user_agent

  @property
  def current(self) -> None: return self._current

  @current.setter
  def current(self, value: int) -> None: self._current = value

  @property
  def prev(self) -> None: return self._prev

  @prev.setter
  def prev(self, value: int) -> None: self._prev = value

  def scrap_follower_count(self) -> int:
    """Scrap and return Twitter user's real time follower count
    """
    for _ in range(SOCIAL_BLADE_SCRAP_LIMIT):
      with requests.get(self.url, headers={"User-Agent": self.user_agent, "Content-Type": "application/json"}) as response:
        if response.status_code == 200: 
          if "application/json" in response.headers.get("Content-Type"):
            if value := int(BeautifulSoup(response.content, "html.parser").text):
              return value
            else: # response.content NOT FOUND
              sys.exit(3)
          # SEARCHING FOR "application/json" else: # "application/json" NOT IN response.headers.get("Content-Type")
        else: # response.status_code NOT 200
          sys.exit(1)
    sys.exit(2)

if __name__ == "__main__":
  """Scrap and print list of most followed Twitter active users 

  :return: Integer indicating fail status, as follows:
    1 : STATUS CODE NOT 200
    2 : WRONG CONTENT TYPE
    3 : CONTENT NOT FOUND
  :rtype: int
  """

  """Fetch Twitter's ranking of most followed active users
  """
  users = []
  with requests.get("https://en.wikipedia.org/wiki/List_of_most-followed_Twitter_accounts") as response:
    if response.status_code == 200:
      if "text/html" in response.headers.get("Content-Type"):
        if ranking_table_rows := BeautifulSoup(response.content, "html.parser").find("table", class_=["wikitable", "sortable", "jquery-tablesorter"]).find('tbody').find_all('tr'):
          idx = 1
          while len(users) < RANKING_LENGTH:
            if table_row := ranking_table_rows[idx]:
              if "—" not in table_row.find('th').text:
                if table_data := table_row.findAll('td'):
                  users.append(TwitterUser(account_name=table_data[1].find('a').text, real_name=table_data[2].find('a').text))
            idx += 1
            if idx > RANKING_ITERATION_LIMIT:
              sys.exit(3)
        else: # ranking_table_rows NOT FOUND
          sys.exit(3) 
      else: # "text/html" NOT IN response.headers.get("Content-Type")
        sys.exit(2)
    else: # response.status_code NOT 200
      sys.exit(1)

  """Print ranking as a table
  """
  table = ""
  while True:
    for idx, user in enumerate(users):
      os.system('clear')
      print(f"{table}\n[{'#' * idx}{'_' * (RANKING_LENGTH - idx)}] {str(idx).rjust(2)}/{RANKING_LENGTH}\n")
      user.current = int(user.scrap_follower_count())

    table = f"Top {RANKING_LENGTH} most followed active Twitter users:\n\n"

    for idx, user in enumerate(users):
      table += f"{str(idx+1).rjust(2)}. {user.real_name}\t@{user.account_name}\t{str(format(user.current, ',')).rjust(11)}".expandtabs(24)
      delta = 0 if user.prev is None else user.current - user.prev
      if delta > 0: table += f"\t{OKGREEN}+{delta:,}{ENDC}"
      elif delta < 0: table += f"\t{FAIL}{delta:,}{ENDC}"
      table += "\n"
      user.prev = user.current