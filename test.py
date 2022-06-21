#!/usr/bin/python3

import typer
from todotxt.todotxt import ToDoTxt

wudju = typer.Typer()

@wudju.command()
def main():
  todo = ToDoTxt("/home/paddex/Documents/todo/todo.txt")
  todo.out()

if __name__ == "__main__":
  wudju()



