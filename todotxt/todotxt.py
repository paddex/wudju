import os
import re

from datetime import datetime

from .todotxt_item import ToDoItem
from config.config import config

class ToDoTxt:

  def __init__(self, file_name: str = "todo.txt"):
    self.dir_location = config["todo"]["dir"]
    self.location = os.path.join(self.dir_location, file_name)

    self.re_complete = re.compile(r"^x\s")
    self.re_dates = re.compile(r"(?:^|(?<=\s))(\d{4}-\d{2}-\d{2})\s")
    self.re_priority = re.compile(r"^\(([A-Z])\)\s+")
    self.re_context = re.compile(r"(?:^|\s+)@(\S+)")
    self.re_projects = re.compile(r"(?:^|\s+)\+(\S+)")

    self.todos = self.parse_file(self.location)


  def add_todo(self, line: str) -> None:
    id = len(self.todos) + 1
    todo_item = self.parse_line(line, id)
    if config["todo"]["insert_date_on_add"]:
      if todo_item.start_date is None:
        todo_item.start_date = datetime.today()
    self.todos.append(todo_item)
    self.todos = self.sort_todos(self.todos)
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
    self.todos = self.sort_todos(self.todos)
    self.write_to_file()


  def undo_todo(self, id: int) -> None:
    todo = self.get_todo_by_id(id)
    if not todo.completed:
      return
    todo.completed = False
    if todo.finish_date is not None:
      todo.finish_date = None
    self.todos = self.sort_todos(self.todos)
    self.write_to_file()


  def edit_todo(self, id: int, new_line: str) -> None:
    todo_item = self.parse_line(new_line, id)
    self.todos[id] = todo_item
    self.todos = self.sort_todos(self.todos)
    self.write_to_file()


  def set_priority(self, id: int, priority: str) -> None:
    todo_item = self.get_todo_by_id(id)
    todo_item.priority = priority
    self.todos = self.sort_todos(self.todos)
    self.write_to_file()


  def show_by_priorities(self, priorities: list[str] = []) -> None:
    if len(priorities) <= 0:
      showlist = self.filter_todos(self.todos, by_has_prio = True)
    else:
      showlist = self.filter_todos(self.todos, by_prio = priorities)

    for todo in showlist:
      print(str(todo.id) + ": " + todo.line)


  def show_projects(self, terms: list[str] = []) -> None:
    projects = self.get_projects(terms)

    for proj in projects:
      print(proj)


  def get_projects(self, terms: list[str] = []) -> list[str]:
    todos = self.todos.copy()
    if len(terms) > 0:
      todos = self.filter_todos(self.todos, by_terms = terms)

    projects = []
    for todo in todos:
      if todo.projects is not None:
        for proj in todo.projects:
          if proj not in projects:
            projects.append(proj)

    return projects


  def show_context(self, terms: list[str] = []):
    context = self.get_context(terms)

    for cxt in context:
      print(cxt)


  def get_context(self, terms: list[str] = []) -> list[str]:
    todos = self.todos.copy()
    if len(terms) > 0:
      todos = self.filter_todos(self.todos, by_terms = terms)

    context = []
    for todo in todos:
      if todo.context is not None:
        for cxt in todo.context:
          if cxt not in context:
            context.append(cxt)

    return context


  def get_todos(self, filter_by: list[str] = None) -> list[ToDoItem]:
    if not filter_by:
      return self.todos


  def get_all_todos(
      self,
      by_terms: list[str] = [],
      by_prio: list[str] = [],
      by_context: list[str] = [],
      by_projects: list[str] = []
  ) -> list[ToDoItem]:
    done_path = os.path.join(self.dir_location, "done.txt")
    archived_todos = self.parse_file(done_path)

    todos = self.todos.copy()
    todos.extend(archived_todos)

    todos = self.filter_todos(todos, by_terms, by_prio, by_context, by_projects)

    todos = self.sort_todos(todos)

    return todos


  def get_todo_by_id(self, id: int) -> ToDoItem:
    for todo in self.todos:
      if todo.id == id:
        return todo

    return None


  def show(
      self,
      by_terms: list[str] = [],
      by_prio: list[str] = [],
      by_context: list[str] = [],
      by_projects: list[str] = [],
  ) -> None:
    showlist = self.filter_todos(self.todos, by_terms, by_prio,
        by_context, by_projects)

    for todo in showlist:
      print(str(todo.id) + ": " + todo.line)


  def show_all(
      self,
      by_terms: list[str] = [],
      by_prio: list[str] = [],
      by_context: list[str] = [],
      by_projects: list[str] = [],
  ) -> None:
    showlist = self.get_all_todos(by_terms, by_prio, by_context, by_projects)

    for todo in showlist:
      print(todo.line)


  def archive(self) -> None:
    completed = []
    not_completed = []
    for todo in self.todos:
      if todo.completed:
        completed.append(todo)
      else:
        not_completed.append(todo)

    self.todos = not_completed

    self.write_to_file()

    with open(os.path.join(self.dir_location, "done.txt"), "a") as done_file:
      for todo in completed:
        done_file.write(todo.line + "\n") 


  def sort_todos(self, todos: list[ToDoItem]) -> list[ToDoItem]:
    todos = sorted(todos, key=lambda todo: todo.line)
    return todos


  def filter_todos(
      self,
      todos: list[ToDoItem],
      by_terms: list[str] = [],
      by_prio: list[str] = [],
      by_context: list[str] = [],
      by_projects: list[str] = [],
      by_has_prio: bool = False
  ) -> list[ToDoItem]:
    filtered_list = todos.copy()

    for word in by_terms:
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

    if len(by_prio) > 0:
      filtered_list = list(
        filter( lambda todo: len(
        [prio for prio in by_prio if prio == todo.priority]) > 0,
        filtered_list)
      )

    if len(by_context) > 0:
      filtered_list = list(
        filter( lambda todo: len(
        [cxt for cxt in by_context if cxt in todo.context]) > 0,
        filtered_list)
      )

    if len(by_projects) > 0:
      filtered_list = list(
        filter( lambda todo: len(
        [proj for proj in by_projects if proj in todo.projects]) > 0,
        filtered_list)
      )

    if by_has_prio:
      filtered_list = list(
        filter( lambda todo: todo.priority is not None, filtered_list)
      )

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


  def parse_file(self, filepath: str) -> list[ToDoItem]:
    todos = []
    if os.path.exists(filepath):
      with open(filepath) as todo_file:
        todo_lines = []
        for line in todo_file:
          todo_lines.append(line.strip())

      todos = self.parse(todo_lines)
      if len(todos) > 1:
        todos = self.sort_todos(todos)

    return todos
