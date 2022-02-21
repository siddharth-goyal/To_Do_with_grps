from asyncio import tasks
from tkinter import FIRST
from tokenize import group
from fastapi import HTTPException, status
from sqlalchemy import delete
from routers.schemas import TodoBase
from sqlalchemy.orm.session import Session
from db.models import DbTodo



def create(db: Session, request: TodoBase, creator_id : int):
  new_todo = DbTodo(
    task = request.task,
    assigned_to = request.assigned_to,
    due_date = request.due_date,
    is_completed = request.is_completed,
    user_id = creator_id,
    group_text = request.group_text,
    group_id =request.group_id
  )
  db.add(new_todo)
  db.commit()
  db.refresh(new_todo)
  return new_todo

def update(id :int ,db: Session, request : TodoBase, creator_id :int):
  get_id= id
  u_id =creator_id
  delete(db, id, creator_id)

  new_todo = DbTodo(
    id = get_id,
    task = request.task,
    assigned_to = request.assigned_to,
    due_date = request.due_date,
    is_completed = request.is_completed,
    user_id = u_id,
    group_text = request.group_text,
    group_id =request.group_id
  )
  db.add(new_todo)
  db.commit()
  db.refresh(new_todo)
  return new_todo


def get_all_todos(db: Session):
  return db.query(DbTodo).all()


def delete(db: Session, id: int ,user_id: int):
  todo = db.query(DbTodo).filter(DbTodo.id == id).first()
  if not todo:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with id {id} not found')
  if todo.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
          detail='Only todo creator can delete post')

  db.delete(todo)
  db.commit()
  return 'ok'

def delete_group(db: Session, group_id: int,user_id: int):
  g_todo=[]
  g_todo= db.query(DbTodo).filter(DbTodo.group_id == group_id).all() 
  if not g_todo:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with group id {group_id} not found')

  flag = 0

  for x in g_todo:
    if x.user_id != user_id:
      flag=1
    else :
      db.delete(x)
      #g_todo.remove(x)
      db.commit()

  if flag==1:
    return 'Some tasks were not deleted due to conficting user'
  else:
    return 'Group Deleted'