import os
import json

def first_time_setup():
  config = {
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
    "greeting": {
      "enabled": "true"
    },
    "styles": {
      "greeting"      : "yellow",
      "quote"         : "blue",
      "quote_author"  : "red",
      "todo_table"    : "white",
      "todo_open"     : "blue",
      "todo_urgent"   : "red",
      "todo_done"     : "green"
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
  config["user"] = name
  config["quote_file"] = quote_location
  config["todo_file"] = todo_location

  write_config()

  return config

def write_config():
  with open(get_config_path(), "w") as config_file:
    config_file.write(json.dumps(config, indent=2))

def get_config_path():
  config_home = get_xdg_config_home()
  if config_home == None:
    config_home = os.path.join(os.getenv("HOME"), ".config")

  config_path = os.path.join(config_home, "wudju")

  if not os.path.exists(config_path):
    os.makedirs(config_path)

  return os.path.join(config_path, "config.json")

def get_xdg_config_home():
  xdg_config_home = os.getenv("XDG_CONFIG_HOME")
  return xdg_config_home

def reset_config():
  if os.path.exists(config_path):
    os.remove(config_path)
  global config
  config = first_time_setup()
  


config_path = get_config_path()

if not os.path.exists(config_path):
  config = first_time_setup()
else:
  try:
    with open(config_path) as cf:
      config = json.load(cf)
  except json.JSONDecodeError as error:
    raise error


