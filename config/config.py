import os
import json

class Config:

  def __init__(self, reset = False):

    config_path = self.get_config_path()
    if reset:
      if os.path.exists(config_path):
        os.remove(config_path)

    if not os.path.exists(config_path):
      self.first_time_setup()
    else:
      try:
        with open(config_path) as cf:
          self.config = json.load(cf)
      except json.JSONDecodeError as error:
        raise error

  def get_config(self):
    return self.config

  def write_config(self):
    with open(self.get_config_path(), "w") as config_file:
      config_file.write(json.dumps(self.config, indent=2))

  def get_config_path(self):
    config_home = self.get_xdg_config_home()
    if config_home == None:
      config_home = os.path.join(os.getenv("HOME"), ".config")

    config_path = os.path.join(config_home, "greeter")

    if not os.path.exists(config_path):
      os.makedirs(config_path)

    return os.path.join(config_path, "config.json")

  def get_xdg_config_home(self):
    xdg_config_home = os.getenv("XDG_CONFIG_HOME")
    return xdg_config_home

  def first_time_setup(self):
    self.config = {
      "colors": {
        "black"   : "#868D80",
        "red"     : "#E68183",
        "green"   : "#A7C080",
        "yellow"  : "#D9BB80",
        "blue"    : "#89BEBA",
        "magenta" : "#D3A0BC",
        "cyan"    : "#87C095",
        "white"   : "#D8CAAC"
      },
      "styles": {
        "greeting"      : "yellow",
        "quote"         : "blue",
        "quote_author"  : "red"
      },
      "quote_file"  : "",
      "todo_file"   : "",
      "user"        : ""
    }

    print("Hello! How may I call you? ")
    name = input()
    print(f"Hi {name}! Where is the quote file you want me to use located?")
    quote_location = input()
    print(f"Lastly, please tell me where I can find your todo.txt file.")
    todo_location = input()
    self.config["user"] = name
    self.config["quote_file"] = quote_location
    self.config["todo_file"] = todo_location

    self.write_config()
