#!/usr/bin/python3

import shutil

from typing import Optional, List

import typer

from todotxt.todotxt import ToDoTxt

wudju = typer.Typer()

@wudju.callback()
def load_todos():
  global todo
  todo = ToDoTxt("/home/paddex/projects/python/wudju/todo_test.txt")

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
def list(
    terms: Optional[List[str]] = typer.Argument(None),
    prio: Optional[List[str]] = typer.Option([]),
    context: Optional[List[str]] = typer.Option([]),
    project: Optional[List[str]] = typer.Option([])
):
  todo.show(terms, prio, context, project)

@wudju.command()
def ls(
    args: Optional[List[str]] = typer.Argument(None),
    prio: Optional[List[str]] = typer.Option(None),
    context: Optional[List[str]] = typer.Option(None),
    project: Optional[List[str]] = typer.Option(None)
):
  list(args, prio, context, project)

@wudju.command()
def listpri(priorities: Optional[List[str]] = typer.Argument(None)):
  todo.show_by_priorities(priorities)

@wudju.command()
def listproj(terms: Optional[List[str]] = typer.Argument(None)):
  todo.show_projects(terms)

@wudju.command()
def reset():
  org_path = "/home/paddex/projects/python/wudju/todo.txt"
  new_path = "/home/paddex/projects/python/wudju/todo_test.txt"
  shutil.copy(org_path, new_path)

if __name__ == "__main__":
  wudju()



