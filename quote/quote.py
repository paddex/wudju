import json
import random

class Quote:

  def __init__(self, quotesFile):
    try:
      with open(quotesFile) as qf:
        self.quotes = json.load(qf)
    except FileNotFoundError as err:
      raise err
    except json.JSONDecodeError as err:
      raise err

  def get_random_quote(self):
    size = len(self.quotes)
    if size < 1:
      return { "quote": "There are no quotes", "author": "greeter", "origin": ""}
    i = random.randint(0, size - 1)
    return self.quotes[i]
