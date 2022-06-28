#!/usr/bin/python3

import json
import datetime
import shutil

import rich.box
from rich.console import Console
from rich.align import Align
from rich.rule import Rule
from rich.table import Table, Column

from typing import Optional, List

import typer

from config.config import config 

from quote.quote import Quote
from todotxt.todotxt import ToDoTxt

console = Console()
wudju = typer.Typer(help="A beautiful terminal start page and todotxt tool.")

@wudju.callback()
def load_todos() -> None:
  global todo
  todo = ToDoTxt()

@wudju.callback(invoke_without_command=True)
def show() -> None:
  global todo 
  todo = ToDoTxt()
  """
  Default command: Shows the greeting, quote and current todo list.
  """
  print_greeting()
  print()
  print_quote()
  print()
  print_todos(["id", "status", "priority", "finish_date", "start_date", "task", "context", "projects"])


@wudju.command("list")
def list_todo(
    terms: Optional[List[str]] = typer.Argument(None),
    prio: Optional[List[str]] = typer.Option([]),
    context: Optional[List[str]] = typer.Option([]),
    project: Optional[List[str]] = typer.Option([])
) -> None:
  """
  Lists all items in the todo.txt file
  """
  todo.show(terms, prio, context, project)


def print_greeting():
  date_now = datetime.datetime.now()
  date_str = date_now.strftime('%d %b %Y | %H:%M')

  user = config["greeting"]["name"]
  greeting_color_setting = config["greeting"]["styles"]["greeting"]
  greeting_color = config["colors"][greeting_color_setting]
  greeting = f"[{greeting_color}] Hallo {user}! {date_str} Uhr"
  center_print(Rule(greeting, style=greeting_color), "bold")
  print()


def print_quote():
  quote_location = config["quote"]["file"]

  quote = get_quote(quote_location)

  quote_color_setting = config["quote"]["styles"]["quote"]
  quote_color = config["colors"][quote_color_setting]

  author_color_setting = config["quote"]["styles"]["author"]
  author_color = config["colors"][author_color_setting]

  origin_color_setting = config["quote"]["styles"]["origin"]
  origin_color = config["colors"][origin_color_setting]

  center_print(f"[{quote_color}] \"{quote['quote']}\"", wrap = True)
  center_print(f"[{author_color}] --{quote['author']}" + 
      f", {quote['origin']}", wrap = True)


def print_todos(cols: list[str] = []):
  todo_items = todo.get_todos()

  todo_table_setting = config["todo"]["styles"]["table"]
  todo_table_color = config["colors"][todo_table_setting]

  todo_table_header_setting = config["todo"]["styles"]["table_header"]
  todo_table_header_color = config["colors"][todo_table_header_setting]

  todo_open_setting = config["todo"]["styles"]["todo_open"]
  todo_open_color = config["colors"][todo_open_setting]

  todo_urgent_setting = config["todo"]["styles"]["todo_urgent"]
  todo_urgent_color = config["colors"][todo_urgent_setting]

  todo_done_setting = config["todo"]["styles"]["todo_done"]
  todo_done_color = config["colors"][todo_done_setting]

  width = shutil.get_terminal_size().columns // 2
  print(width)

  id_col = Column("ID")
  status_col = Column("Status")
  pri_col = Column("Priority")
  finish_date_col = Column("Finish Date")
  start_date_col = Column("Start Date")
  task_col = Column("Task", width=30)
  context_col = Column("Context")
  projects_col = Column("Projects")

  table_headers = []
  if len(cols) > 0:
    if "id" in cols:
      table_headers.append(id_col)
    if "pri" in cols:
      table_headers.append(pri_col)
    if "task" in cols:
      table_headers.append(task_col)
    if "start_date" in cols:
      table_headers.append(start_date_col)
    if "finish_date" in cols:
      table_headers.append(finish_date_col)
    if "context" in cols:
      table_headers.append(context_col)
    if "projects" in cols:
      table_headers.append(projects_col)
    if "status" in cols:
      table_headers.append(status_col)
  else:
    table_headers = [id_col, task_col, status_col]

  table = Table(
    *table_headers,
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

  color = todo_open_color
  for item in todo_items:
    if item.completed:
      item_status = "✅"
      color = todo_done_color
    else:
      item_status = "❌"

    task_id = f"[{color}] {item.id}"
    task_status = f"[{color}] {item_status}"
    task_priority = f"[{color}] {item.priority}"
    task_finish_date = f"[{color}] {item.finish_date}"
    task_start_date = f"[{color}] {item.start_date}"
    task_text = f"[{color}] {item.text}"
    task_context = f"[{color}] {item.context}"
    task_projects = f"[{color}] {item.projects}"

    cols = [task_id, task_text, task_status]
    table.add_row(*cols)

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


if __name__ == "__main__":
  wudju()

