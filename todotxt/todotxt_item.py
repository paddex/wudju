from datetime import date

class ToDoItem:

  def __init__(self, id: int, completed: bool = False, priority: str = None, \
      finish_date: date = None, start_date: date = None, text: str = None, \
      context: list = [], projects: list = []):
    
    self.id = id
    self.completed = completed
    self.priority = priority
    self.finish_date = finish_date
    self.start_date = start_date
    self.text = text
    self.context = context
    self.projects = projects

  def get_string(self):
    line = ""
    if self.completed:
      line = line + "x "

    if self.priority is not None:
      line = line + self.priority + " "

    if self.finish_date is not None:
      line = line + self.finish_date.strftime("%Y-%m-%d ")

    if self.start_date is not None:
      line = line + self.start_date.strftime("%Y-%m-%d ")

    if self.text is not None:
      line = line + self.text

    return line
      

