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
      "white"   : "#D8CAAC",
      "fg_light": "#fffacd",
      "fg_dark" : "#2B3239"
    },
    "greeting": {
      "enabled": "true",
      "name": "",
      "styles": {
        "greeting": "yellow",
      },
    },
    "quote": {
      "enable": "true",
        "file": "",
        "styles": {
          "quote": "blue",
          "author": "red",
          "origin": "red",
        },
    },
    "todo": {
      "enable": "true",
      "dir": "",
      "hide_projects": "true",
      "hide_context": "true",
      "insert_date_on_add": "true",
      "insert_date_on_complete": "true",
      "styles": {
        "table_border": "white",
        "table_header": "cyan",
        "table_todo_open": "blue",
        "table_todo_urgent": "red",
        "table_todo_done": "green",
        "cmd_add_bg": "blue",
        "cmd_add_fg": "fg_dark",
        "cmd_rm_bg": "blue",
        "cmd_rm_fg": "fg_dark",
        "cmd_do_bg": "green",
        "cmd_do_fg": "fg_dark",
        "cmd_undo_bg": "green",
        "cmd_undo_fg": "fg_dark",
        "cmd_archive_bg": "green",
        "cmd_archive_fg": "fg_dark",
        "cmd_pri_bg": "green",
        "cmd_pri_fg": "fg_dark"
      },
    },
  }

  print("Hello! How may I call you? ")
  name = input()
  print(f"Hi {name}! Where is the quote file you want me to use located?")
  quote_location = input()
  print(f"Lastly, please tell me where I can find your todo.txt file.")
  todo_location = input()
  config["greeting"]["name"] = name
  config["quote"]["file"] = quote_location
  config["todo"]["dir"] = todo_location

  write_config(config)

  return config

  
def write_config(config):
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


def confirm_prompt(msg: str, default: str = "yes") -> bool:

  valid = {"yes": True, "ye": True, "y": True, "no": False, "n": False}

  if default is None:
    prompt = " [y/n]: "
  elif default == "yes":
    prompt = " [Y/n]: "
  elif default == "no":
    prompt = " [y/N]: "
  else:
    raise ValueError("invalid default value: '%s'" % default)

  while True:
    print(msg + prompt)
    inp = input().lower()

    if default is not None and inp == "":
      return valid[default]
    elif inp in valid:
      return valid[inp]
    else:
      print("Please responsd with 'yes' or 'no'")


config_path = get_config_path()

if not os.path.exists(config_path):
  config = first_time_setup()
else:
  try:
    with open(config_path) as cf:
      config = json.load(cf)
  except json.JSONDecodeError as error:
    confirm = confirm_prompt("Would you like to reset your config?")
    if confirm:
      reset_config()
    else:
      exit(1)


