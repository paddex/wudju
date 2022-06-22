import os
import re

from datetime import datetime

from .todotxt_item import ToDoItem
from config.config import config

class ToDoTxt:

  def __init__(self, todo_location: str):
    self.location = todo_location

    self.re_complete = re.compile(r"^x\s")
    self.re_dates = re.compile(r"(?:^|(?<=\s))(\d{4}-\d{2}-\d{2})\s")
    self.re_priority = re.compile(r"^\(([A-Z])\)\s+")
    self.re_context = re.compile(r"(?:^|\s+)@(\S+)")
    self.re_projects = re.compile(r"(?:^|\s+)\+(\S+)")

    self.todos = []
    if os.path.exists(todo_location):
      with open(todo_location) as todo_file:
        todo_lines = []
        for line in todo_file:
          todo_lines.append(line.strip())

      self.todos = self.parse(todo_lines)
      if len(self.todos) > 1:
        self.sort_todos()

  def add_todo(self, line: str) -> None:
    id = len(self.todos) + 1
    todo_item = self.parse_line(line, id)
    if config["todo"]["insert_date_on_add"]:
      if todo_item.start_date is None:
        todo_item.start_date = datetime.today()
    self.todos.append(todo_item)
    self.sort_todos()
    self.write_to_file()

  def delete_todo(self, id: int) -> None:
    todo = self.get_todo_by_id(id)
    self.todos.remove(todo)
    self.write_to_file()

  def complete_todo(self, id: int) -> None:
    todo = self.get_todo_by_id(id)
    if todo.completed:
      return
    todo.completed = True
    todo.priority = None
    if config["todo"]["insert_date_on_complete"]:
      if todo.start_date is not None:
        todo.finish_date = datetime.today()
    self.sort_todos()
    self.write_to_file()

  def undo_todo(self, id: int) -> None:
    todo = self.get_todo_by_id(id)
    if not todo.completed:
      return
    todo.completed = False
    if todo.finish_date is not None:
      todo.finish_date = None
    self.sort_todos()
    self.write_to_file()

  def get_todos(self, filter_by: list[str] = None) -> list[ToDoItem]:
    if not filter_by:
      return self.todos

  def get_todo_by_id(self, id: int) -> ToDoItem:
    for todo in self.todos:
      if todo.id == id:
        return todo

    return None

  def show(
      self,
      filter_by_terms: list[str] = None,
      filter_by_prio: list[str] = None,
      filter_by_context: list[str] = None,
      filter_by_projects: list[str] = None
  ) -> list[ToDoItem]:
    showlist = self.filter_todos(
        filter_by_terms,
        filter_by_prio,
        filter_by_context,
        filter_by_projects)

    for todo in showlist:
      print(str(todo.id) + ": " + todo.line)

  def sort_todos(self) -> None:
    self.todos = sorted(self.todos, key=lambda todo: todo.line)

  def filter_todos(
      self,
      filter_by_terms: list[str] = None,
      filter_by_prio: list[str] = None,
      filter_by_context: list[str] = None,
      filter_by_projects: list[str] = None
  ) -> list[ToDoItem]:
    filtered_list = self.todos.copy()
    for word in filter_by_terms:
      if "|" in word:
        words = word.split("|")
        filtered_list = list(filter(
          lambda todo: len(
            [w for w in words if w in todo.line]) > 0, filtered_list))
      elif word.startswith("%"):
        word = word.replace("%", "")
        filtered_list = list(filter(
          lambda todo: not word in todo.line, filtered_list))
      else: 
        filtered_list = list(filter(
          lambda todo: word in todo.line, filtered_list))

    filtered_list = list(
      filter( lambda todo: len(
      [prio for prio in filter_by_prio if prio == todo.priority]) > 0,
      filtered_list)
    )

    for cxt in filter_by_context:
      filtered_list = list(filter(
        lambda todo: cxt in todo.context, filtered_list))

    for proj in filter_by_projects:
      filtered_list = list(filter(
        lambda todo: proj in todo.projects, filtered_list))

    return filtered_list

  def write_to_file(self) -> None:
    with open(self.location, "w") as todo_file:
      for todo in self.todos:
        todo_file.write(todo.line + "\n")

  def parse(self, lines: list[str]) -> list[ToDoItem]:
    todos = []
    i = 0
    for line in lines:
      i = i + 1
      todo_item = self.parse_line(line, i)
      todos.append(todo_item)

    return todos

  def parse_line(self, line: str, id: int) -> ToDoItem:
    completed = False
    priority = None
    finish_date = None
    start_date = None
    text = None
    context = []
    projects = []

    if self.re_complete.search(line) is not None:
      line = self.re_complete.sub("", line, 1)
      completed = True

    if not completed:
      match = self.re_priority.search(line) 
      if match is not None:
        line = self.re_priority.sub("", line, 1)
        priority = match.group(1)

    matches = self.re_dates.findall(line)
    if len(matches) > 0:
      if len(matches) > 1:
        finish = matches[0]
        start = matches[1]
        finish_date = datetime.strptime(finish, "%Y-%m-%d")
        start_date = datetime.strptime(start, "%Y-%m-%d")
        line = self.re_dates.sub("", line, 2)
      else:
        start = matches[0]
        start_date = datetime.strptime(start, "%Y-%m-%d")
        line = self.re_dates.sub("", line, 1)

    matches = self.re_context.findall(line)
    for match in matches:
      context.append(match)

    if config["todo"]["hide_context"]:
      line = self.re_context.sub("", line)

    matches = self.re_projects.findall(line)
    for match in matches:
      projects.append(match)

    if config["todo"]["hide_projects"]:
      line = self.re_projects.sub("", line)

    text = line.strip()

    todo_item = ToDoItem(id, completed, priority, finish_date, start_date, text, 
        context, projects)

    return todo_item
