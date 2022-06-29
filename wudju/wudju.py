#!/usr/bin/python3

import json
import datetime
import shutil
import re

import rich.box
from rich.console import Console
from rich.align import Align
from rich.rule import Rule
from rich.table import Table, Column

from typing import Optional, List

import typer

from .config.config import config 

from .quote.quote import Quote
from .todotxt.todotxt import ToDoTxt
from .todotxt.todotxt_item import ToDoItem

console = Console()
wudju = typer.Typer(help="A beautiful terminal start page and todotxt tool.")

@wudju.callback(invoke_without_command=True)
def show(
    ctx: typer.Context,
    col_id: bool = typer.Option(True, "--id", "-i", help="Shows ID column"),
    col_pri: bool = typer.Option(True, "--priority", "-p",
      help="Shows priority column"),
    col_task: bool = typer.Option(True, "--task", "-t", 
      help="Shows task column"),
    col_status: bool = typer.Option(True, "--status", "-s",
      help="Shows status column"),
    col_finish_date: bool = typer.Option(False, "--finish-date", "-f",
      help="Shows finish date column"),
    col_start_date: bool = typer.Option(False, "--start-date", "-d",
      help="Shows start date column"),
    col_context: bool = typer.Option(False, "--context", "-c",
      help="Shows context column"),
    col_projects: bool = typer.Option(False, "--projects",
      help="Shows projects column")
) -> None:

  global todo 
  todo = ToDoTxt()

  if ctx.invoked_subcommand is not None:
    return

  columns = []
  if col_id:
    columns.append("id")
  if col_pri:
    columns.append("priority")
  if col_task:
    columns.append("task")
  if col_status:
    columns.append("status")
  if col_finish_date:
    columns.append("finish_date")
  if col_start_date:
    columns.append("start_date")
  if col_context:
    columns.append("context")
  if col_projects:
    columns.append("projects")

  print_greeting()
  print()
  print_quote()
  print()
  todos = todo.get_todos()
  print_todos(todos, columns)


@wudju.command("list")
def list_todo(
    terms: Optional[List[str]] = typer.Argument(None, 
      help="Filter list by terms"),
    prio: Optional[List[str]] = typer.Option([],
      help="Filter list by priority"),
    context: Optional[List[str]] = typer.Option([],
      help="Filter list by context"),
    projects: Optional[List[str]] = typer.Option([],
      help="Filter list by projects"),
    col_id: bool = typer.Option(True, "--show-id", "-i", help="Shows ID column"),
    col_pri: bool = typer.Option(True, "--show-priority", "-p",
      help="Shows priority column"),
    col_task: bool = typer.Option(True, "--show-task", "-t", 
      help="Shows task column"),
    col_status: bool = typer.Option(True, "--show-status", "-s",
      help="Shows status column"),
    col_finish_date: bool = typer.Option(False, "--show-finish-date", "-f",
      help="Shows finish date column"),
    col_start_date: bool = typer.Option(False, "--show-start-date", "-d",
      help="Shows start date column"),
    col_context: bool = typer.Option(False, "--show-context", "-c",
      help="Shows context column"),
    col_projects: bool = typer.Option(False, "--show-projects",
      help="Shows projects column")
) -> None:
  """ Lists all items (or a filtered selection) in the todo.txt file """

  columns = []
  if col_id:
    columns.append("id")
  if col_pri:
    columns.append("priority")
  if col_task:
    columns.append("task")
  if col_status:
    columns.append("status")
  if col_finish_date:
    columns.append("finish_date")
  if col_start_date:
    columns.append("start_date")
  if col_context:
    columns.append("context")
  if col_projects:
    columns.append("projects")

  todos = todo.get_todos(terms, prio, context, projects)

  print_todos(todos, columns)


@wudju.command()
def add(todo_str: str) -> None:
  """ Adds a todo to the todo.txt file """
  todo.add_todo(todo_str)


@wudju.command()
def rm(id: int) -> None:
  """ Removes a todo from the todo.txt file """
  todo.delete_todo(id)


@wudju.command()
def do(id: int) -> None:
  """
  Marks a todo as completed
  """
  todo.complete_todo(id)


@wudju.command()
def undo(id: int) -> None:
  """Marks a completed todo as not completed"""
  todo.undo_todo(id)


@wudju.command()
def edit(id: int, new_todo: str) -> None:
  """Replaces the chosen todo with the new one"""
  todo.edit_todo(id - 1, new_todo)


@wudju.command()
def pri(id: int, priority: str = typer.Argument(None)) -> None:
  """Adds or removes a priority from the chosen todo"""
  if priority is not None:
    pri = re.compile("^[A-Z]$")
    if pri.fullmatch(priority) is None:
      typer.echo("Not a valid priority. Must be between A and Z.")
      raise typer.Exit(1)
  todo.set_priority(id, priority)


@wudju.command()
def listall(
    terms: Optional[List[str]] = typer.Argument(None),
    prio: Optional[List[str]] = typer.Option([]),
    context: Optional[List[str]] = typer.Option([]),
    projects: Optional[List[str]] = typer.Option([]),
    col_pri: bool = typer.Option(True, "--show-priority", "-p",
      help="Shows priority column"),
    col_task: bool = typer.Option(True, "--show-task", "-t", 
      help="Shows task column"),
    col_status: bool = typer.Option(True, "--show-status", "-s",
      help="Shows status column"),
    col_finish_date: bool = typer.Option(False, "--show-finish-date", "-f",
      help="Shows finish date column"),
    col_start_date: bool = typer.Option(False, "--show-start-date", "-d",
      help="Shows start date column"),
    col_context: bool = typer.Option(False, "--show-context", "-c",
      help="Shows context column"),
    col_projects: bool = typer.Option(False, "--show-projects",
      help="Shows projects column")
) -> None:
  """Lists all todos from todo.txt and done.txt"""
  columns = []
  if col_pri:
    columns.append("priority")
  if col_task:
    columns.append("task")
  if col_status:
    columns.append("status")
  if col_finish_date:
    columns.append("finish_date")
  if col_start_date:
    columns.append("start_date")
  if col_context:
    columns.append("context")
  if col_projects:
    columns.append("projects")

  todos = todo.get_all_todos(terms, prio, context, projects)

  print_todos(todos, columns)


@wudju.command()
def listpri(
    priorities: Optional[List[str]] = typer.Argument(None),
    col_id: bool = typer.Option(True, "--show-id", "-i", help="Shows ID column"),
    col_pri: bool = typer.Option(True, "--show-priority", "-p",
      help="Shows priority column"),
    col_task: bool = typer.Option(True, "--show-task", "-t", 
      help="Shows task column"),
    col_status: bool = typer.Option(True, "--show-status", "-s",
      help="Shows status column"),
    col_finish_date: bool = typer.Option(False, "--show-finish-date", "-f",
      help="Shows finish date column"),
    col_start_date: bool = typer.Option(False, "--show-start-date", "-d",
      help="Shows start date column"),
    col_context: bool = typer.Option(False, "--show-context", "-c",
      help="Shows context column"),
    col_projects: bool = typer.Option(False, "--show-projects",
      help="Shows projects column")
)-> None:
  """List all todos with the chosen priority(ies)"""
  columns = []
  if col_id:
    columns.append("id")
  if col_pri:
    columns.append("priority")
  if col_task:
    columns.append("task")
  if col_status:
    columns.append("status")
  if col_finish_date:
    columns.append("finish_date")
  if col_start_date:
    columns.append("start_date")
  if col_context:
    columns.append("context")
  if col_projects:
    columns.append("projects")

  todos = todo.get_by_priorities(priorities)
  print_todos(todos, columns)


@wudju.command()
def listproj(terms: Optional[List[str]] = typer.Argument(None)) -> None:
  """List all projects"""
  projects = todo.get_projects(terms)
  tbl = Table("Projects (+)")
  for project in projects:
    tbl.add_row(project)

  center_print(tbl)


@wudju.command()
def listcon(terms: Optional[List[str]] = typer.Argument(None)) -> None:
  """List every context"""
  context = todo.get_context(terms)
  tbl = Table("Context (@)")
  for cxt in context:
    tbl.add_row(cxt)

  center_print(tbl)


@wudju.command()
def archive() -> None:
  """Move all completed todos to done.txt"""
  todo.archive()


def print_greeting() -> None:
  date_now = datetime.datetime.now()
  date_str = date_now.strftime('%d %b %Y | %H:%M')

  user = config["greeting"]["name"]
  greeting_color_setting = config["greeting"]["styles"]["greeting"]
  greeting_color = config["colors"][greeting_color_setting]
  greeting = f"[{greeting_color}] Hallo {user}! {date_str} Uhr"
  center_print(Rule(greeting, style=greeting_color), "bold")
  print()


def print_quote() -> None:
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
      f", [{origin_color}]{quote['origin']}", wrap = True)


def print_todos(todo_items: list[ToDoItem], cols: list[str]) -> None:

  todo_open_setting = config["todo"]["styles"]["todo_open"]
  todo_open_color = config["colors"][todo_open_setting]

  todo_urgent_setting = config["todo"]["styles"]["todo_urgent"]
  todo_urgent_color = config["colors"][todo_urgent_setting]

  todo_done_setting = config["todo"]["styles"]["todo_done"]
  todo_done_color = config["colors"][todo_done_setting]

  table = create_table(todo_items, cols)


  color = todo_open_color
  for item in todo_items:
    if item.completed:
      item_status = "✅"
      color = todo_done_color
    else:
      item_status = "❌"

    task_id = f"[{color}]{item.id}"
    task_status = f"[{color}]{item_status}"
    if item.priority is not None:
      task_priority = f"[{color}]{item.priority}"
    else:
      task_priority = f"[{color}]"
    if item.finish_date is not None:
      task_finish_date = f"[{color}]{item.finish_date.strftime('%d.%m.%Y')}"
    else:
      task_finish_date = f"[{color}]-"
    if item.start_date is not None:
      task_start_date = f"[{color}]{item.start_date.strftime('%d.%m.%Y')}"
    else:
      task_start_date = f"[{color}]-"
    task_text = f"[{color}]{item.text}"
    task_context = f"[{color}]{', '.join(item.context)}"
    task_projects = f"[{color}]{', '.join(item.projects)}"

    row_values = []
    if len(cols) > 0:
      if "id" in cols:
        row_values.append(task_id)
      if "priority" in cols:
        row_values.append(task_priority)
      if "task" in cols:
        row_values.append(task_text)
      if "start_date" in cols:
        row_values.append(task_start_date)
      if "finish_date" in cols:
        row_values.append(task_finish_date)
      if "context" in cols:
        row_values.append(task_context)
      if "projects" in cols:
        row_values.append(task_projects)
      if "status" in cols:
        row_values.append(task_status)

    table.add_row(*row_values)

  center_print(table)


def create_table(todos: list[ToDoItem], cols: list[str]) -> Table:
  todo_table_setting = config["todo"]["styles"]["table"]
  todo_table_color = config["colors"][todo_table_setting]

  todo_table_header_setting = config["todo"]["styles"]["table_header"]
  todo_table_header_color = config["colors"][todo_table_header_setting]

  terminal_width = shutil.get_terminal_size().columns
  min_width = terminal_width // 2
  max_width = terminal_width - 20

  if terminal_width < 150:
    max_cw = 10
    max_pw = 10
  elif terminal_width < 300:
    max_cw = 20
    max_pw = 20
  else:
    max_cw = 30
    max_pw = 30

  context_width = 0
  projects_width = 0
  task_width = 0
  for todo_item in todos:
    cw = len(", ".join(todo_item.context))
    pw = len(", ".join(todo_item.projects))
    tw = len(todo_item.text)
    if cw > context_width:
      context_width = cw
    if pw > projects_width:
      projects_width = pw
    if tw > task_width:
      task_width = tw

  if context_width > max_cw:
    context_width = max_cw
  if projects_width > max_pw:
    projects_width = max_pw

  ID_WIDTH = 3
  STATUS_WIDTH = 6
  DATES_WIDTH = 10
  PRI_WIDTH = 3
  CONTEXT_WIDTH = context_width
  PROJECTS_WIDTH = projects_width
  TASK_WIDTH = 40

  current_width = 0
  if "id" in cols:
    current_width = current_width + ID_WIDTH
  if "priority" in cols:
    current_width = current_width + PRI_WIDTH
  if "task" in cols:
    current_width = current_width + TASK_WIDTH
  if "start_date" in cols:
    current_width = current_width + DATES_WIDTH
  if "finish_date" in cols:
    current_width = current_width + DATES_WIDTH
  if "context" in cols:
    current_width = current_width + CONTEXT_WIDTH
  if "projects" in cols:
    current_width = current_width + PROJECTS_WIDTH
  if "status" in cols:
    current_width = current_width + STATUS_WIDTH

  if current_width < min_width:
    delta = (min_width - current_width)
    TASK_WIDTH = TASK_WIDTH + delta
    current_width = current_width + delta

  if task_width > TASK_WIDTH:
    if current_width < max_width:
      if (current_width + (task_width - TASK_WIDTH) < max_width):
        TASK_WIDTH = TASK_WIDTH + (task_width - TASK_WIDTH)
      else:
        TASK_WIDTH = TASK_WIDTH + (max_width - current_width)

  id_col = Column("ID", width=ID_WIDTH)
  status_col = Column("Status", width=STATUS_WIDTH)
  pri_col = Column("Pri", width=PRI_WIDTH)
  finish_date_col = Column("Finish Date", width=DATES_WIDTH)
  start_date_col = Column("Start Date", width=DATES_WIDTH)
  task_col = Column("Task", width=TASK_WIDTH)
  context_col = Column("Context", width=CONTEXT_WIDTH)
  projects_col = Column("Projects", width=PROJECTS_WIDTH)

  table_headers = []
  if "id" in cols:
    table_headers.append(id_col)
  if "priority" in cols:
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

  table = Table(
    *table_headers,
    title = "Here are your Tasks:",
    title_style = todo_table_color,
    header_style = todo_table_header_color,
    style = todo_table_color,
    box = rich.box.SIMPLE_HEAVY,
    padding = (1, 1),
    collapse_padding = True,
    show_lines = False
  )

  return table


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

