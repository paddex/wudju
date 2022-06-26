#!/usr/bin/python3

import shutil
import re

from typing import Optional, List

import typer

from todotxt.todotxt import ToDoTxt

wudju = typer.Typer()

@wudju.callback()
def load_todos():
  global todo
  todo = ToDoTxt()

@wudju.command()
def add(todo_str: str):
  todo.add_todo(todo_str)

@wudju.command()
def delete(id: int):
  todo.delete_todo(id)

@wudju.command()
def do(id: int):
  todo.complete_todo(id)

@wudju.command()
def undo(id: int):
  todo.undo_todo(id)

@wudju.command()
def edit(id: int, new_line: str):
  todo.edit_todo(id - 1, new_line)

@wudju.command()
def pri(id: int, priority: str = typer.Argument(None)):
  if priority is not None:
    pri = re.compile("^[A-Z]$")
    if pri.fullmatch(priority) is None:
      typer.echo("Not a valid priority. Must be between A and Z.")
      raise typer.Exit(1)
  todo.set_priority(id, priority)

@wudju.command()
def list(
    terms: Optional[List[str]] = typer.Argument(None),
    prio: Optional[List[str]] = typer.Option([]),
    context: Optional[List[str]] = typer.Option([]),
    project: Optional[List[str]] = typer.Option([])
):
  todo.show(terms, prio, context, project)

@wudju.command()
def ls(
    terms: Optional[List[str]] = typer.Argument(None),
    prio: Optional[List[str]] = typer.Option([]),
    context: Optional[List[str]] = typer.Option([]),
    project: Optional[List[str]] = typer.Option([])
):
  list(terms, prio, context, project)

@wudju.command()
def listall(
    terms: Optional[List[str]] = typer.Argument(None),
    prio: Optional[List[str]] = typer.Option([]),
    context: Optional[List[str]] = typer.Option([]),
    project: Optional[List[str]] = typer.Option([])
):
  todo.show_all(terms, prio, context, project)

@wudju.command()
def listpri(priorities: Optional[List[str]] = typer.Argument(None)):
  todo.show_by_priorities(priorities)

@wudju.command()
def listproj(terms: Optional[List[str]] = typer.Argument(None)):
  todo.show_projects(terms)

@wudju.command()
def listcon(terms: Optional[List[str]] = typer.Argument(None)):
  todo.show_context(terms)

@wudju.command()
def archive():
  todo.archive()

@wudju.command()
def reset():
  org_path = "/home/paddex/projects/python/wudju/todo_bak.txt"
  new_path = "/home/paddex/projects/python/wudju/todo.txt"
  shutil.copy(org_path, new_path)

if __name__ == "__main__":
  wudju()



