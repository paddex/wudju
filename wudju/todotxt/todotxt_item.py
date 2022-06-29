from datetime import date
from ..config.config import config

class ToDoItem:

  def __init__(self, id: int, completed: bool = False, priority: str = None, \
      finish_date: date = None, start_date: date = None, text: str = None, \
      context: list = [], projects: list = []):
    
    self._id = id
    self._completed = completed
    self._priority = priority
    self._finish_date = finish_date
    self._start_date = start_date
    self._text = text
    self._context = context
    self._projects = projects
    self._line = self.get_string()


  def get_string(self) -> str:
    line = ""
    if self.completed:
      line = line + "x "

    if self.priority is not None:
      line = line + "(" + self.priority + ") "

    if self.finish_date is not None:
      line = line + self.finish_date.strftime("%Y-%m-%d ")

    if self.start_date is not None:
      line = line + self.start_date.strftime("%Y-%m-%d ")

    if self.text is not None:
      line = line + self.text

    if config["todo"]["hide_context"]:
      for cxt in self.context:
        line = line + " @" + cxt

    if config["todo"]["hide_projects"]:
      for project in self.projects:
        line = line + " +" + project

    return line

  @property
  def id(self):
    return self._id

  @id.setter
  def id(self, new_id):
    self._id = new_id
    self._line = self.get_string()

  @property
  def completed(self):
    return self._completed

  @completed.setter
  def completed(self, new_cmpl):
    self._completed = new_cmpl
    self._line = self.get_string()

  @property
  def priority(self):
    return self._priority

  @priority.setter
  def priority(self, new_pri):
    self._priority = new_pri
    self._line = self.get_string()

  @property
  def finish_date(self):
    return self._finish_date

  @finish_date.setter
  def finish_date(self, new_f_date):
    self._finish_date = new_f_date
    self._line = self.get_string()

  @property
  def start_date(self):
    return self._start_date

  @start_date.setter
  def start_date(self, new_s_date):
    self._start_date = new_s_date
    self._line = self.get_string()

  @property
  def text(self):
    return self._text

  @text.setter
  def text(self, new_text):
    self._text = new_text
    self._line = self.get_string()

  @property
  def context(self):
    return self._context

  @context.setter
  def context(self, new_cxt):
    self._context = new_cxt
    self._line = self.get_string()

  @property
  def projects(self):
    return self._projects

  @projects.setter
  def projects(self, new_proj):
    self._projects = new_proj
    self._line = self.get_string()

  @property
  def line(self):
    return self._line

  @line.setter
  def line(self, new_line):
    self._line = new_line
    self._line = self.get_string()
