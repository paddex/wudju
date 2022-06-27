#!/usr/bin/python3

import os
import sys
import json
import datetime
import shutil

import rich.box
from rich.console import Console
from rich.align import Align
from rich.rule import Rule
from rich.table import Table
from rich.prompt import Confirm

import typer

from config.config import config 

from quote.quote import Quote
from todotxt.todotxt import ToDoTxt

console = Console()
wudju = typer.Typer()

def show(config):
  print_greeting(config)
  print()
  print_quote(config)
  print()
  print_todos(config)

def print_greeting(config):
  date_now = datetime.datetime.now()
  date_str = date_now.strftime('%d %b %Y | %H:%M')

  user = config["user"]
  greeting_color_setting = config["styles"]["greeting"]
  greeting_color = config["colors"][greeting_color_setting]
  greeting = f"[{greeting_color}] Hallo {user}! {date_str} Uhr"
  center_print(Rule(greeting, style=greeting_color), "bold")
  print()

def print_quote(config):
  quote_location = config["quote_file"]

  quote = get_quote(quote_location)

  quote_color_setting = config["styles"]["quote"]
  quote_color = config["colors"][quote_color_setting]

  author_color_setting = config["styles"]["quote_author"]
  author_color = config["colors"][author_color_setting]

  center_print(f"[{quote_color}] \"{quote['quote']}\"", wrap = True)
  center_print(f"[{author_color}] --{quote['author']}" + 
      f", {quote['origin']}", wrap = True)

def print_todos(config):
  todo_location = config["todo_file"]
  todo = ToDoTxt(todo_location)

  todo_items = todo.get_todos()

  todo_table_setting = config["styles"]["todo_table"]
  todo_table_color = config["colors"][todo_table_setting]

  todo_table_header_setting = config["styles"]["todo_table_header"]
  todo_table_header_color = config["colors"][todo_table_header_setting]

  todo_open_setting = config["styles"]["todo_open"]
  todo_open_color = config["colors"][todo_open_setting]

  todo_urgent_setting = config["styles"]["todo_urgent"]
  todo_urgent_color = config["colors"][todo_urgent_setting]

  todo_done_setting = config["styles"]["todo_done"]
  todo_done_color = config["colors"][todo_done_setting]

  width = shutil.get_terminal_size().columns // 2

  table = Table(
    title = "Here are your Tasks:",
    title_style = todo_table_color,
    header_style = todo_table_header_color,
    style = todo_table_color,
    width = width,
    box = rich.box.SIMPLE_HEAVY,
    padding = (1, 1),
    collapse_padding = True,
    show_lines = False
  )

  table.add_column("ID")
  table.add_column("Task")
  table.add_column("Status")

  color = todo_open_color
  for item in todo_items:
    if item.completed:
      item_status = "✅"
      color = todo_done_color
    else:
      item_status = "❌"

    task_index = f"[{color}] {item.id}"
    task_text = f"[{color}] {item.text}"
    task_status = f"[{color}] {item_status}"

    table.add_row(task_index, task_text, task_status)

  center_print(table)

def center_print(text: str, style: str = None, wrap: bool = False) -> None:
  width = shutil.get_terminal_size().columns

  if wrap:
    width = width // 2

  console.print(Align.center(text, style=style, width=width, pad= False))

def get_quote(quote_location) -> dict:
  try: 
    quoteObj = Quote(quote_location)
    quote = quoteObj.get_random_quote()
  except FileNotFoundError:
    quote = {
        "quote": "Error: Quote file could not be found.",
        "author": "wudju.py",
        "origin": "-"
    }
  except json.JSONDecodeError:
    quote = {
        "quote": "Error: Quote file could not be parsed.",
        "author": "wudju.py",
        "origin": "-"
    }

  return quote

def main():

  config = cfg_module.config

  show(config)

if __name__ == "__main__":

  main()

