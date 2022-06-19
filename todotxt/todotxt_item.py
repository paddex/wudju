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
