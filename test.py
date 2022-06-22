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
    prio: Optional[List[str]] = typer.Option(None),
    context: Optional[List[str]] = typer.Option(None),
    projects: Optional[List[str]] = typer.Option(None)
):
  todo.show(terms, prio, context, projects)

@wudju.command()
def ls(
    args: Optional[List[str]] = typer.Argument(None),
    prio: Optional[List[str]] = typer.Option(None),
    context: Optional[List[str]] = typer.Option(None),
    projects: Optional[List[str]] = typer.Option(None)
):
  list(args, prio, context, projects)

@wudju.command()
def reset():
  org_path = "/home/paddex/projects/python/wudju/todo.txt"
  new_path = "/home/paddex/projects/python/wudju/todo_test.txt"
  shutil.copy(org_path, new_path)

if __name__ == "__main__":
  wudju()



