from tokenize import group
from fastapi import HTTPException, status
from routers.schemas import TodoBase
from sqlalchemy.orm.session import Session
from db.models import DbTodo



def create(db: Session, request: TodoBase):
  new_todo = DbTodo(
    task = request.task,
    assigned_to = request.assigned_to,
    due_date = request.due_date,
    is_completed = request.is_completed,
    user_id = request.creator_id,
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

def delete_group(db: Session, group_id: int):#,user_id: int):
  g_todo=[]
  g_todo= db.query(DbTodo).filter(DbTodo.group_id == group_id).all()
  if not g_todo:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with group id {group_id} not found')
  # if g_todo.user_id != user_id:
  #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
  #         detail='Only todo group creator can delete task')

  while(g_todo):
    db.delete(g_todo[0])
    g_todo.pop(0)
    db.commit()
  return 'Group is deleted'