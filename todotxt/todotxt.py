import os
import re
from datetime import datetime

from .todotxt_item import ToDoItem

class ToDoTxt:

  def __init__(self, todo_location):
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

  def get_todos(self, filter: dict = None):
    if not filter:
      return self.todos

  def parse(self, lines) -> list:
    todos = []
    i = 0
    for line in lines:
      i = i + 1
      todo_item = self.parse_line(line, i)
      todos.append(todo_item)

    return todos

  def parse_line(self, line, id) -> ToDoItem:
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

    matches = self.re_projects.findall(line)
    for match in matches:
      projects.append(match)

    text = line

    todo_item = ToDoItem(id, completed, priority, finish_date, start_date, text, 
        context, projects)

    return todo_item
