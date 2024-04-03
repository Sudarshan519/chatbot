 
import json
from fastapi import FastAPI, File, Form, HTTPException, Depends, Request, UploadFile
from typing import Annotated, Dict, List, Optional
from fastapi.security import HTTPBasic
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.routing import APIRouter
import uvicorn

# from ai_tools_app.get_user import get_current_username,get_current_user_from_bearer
from ai_tools_app.models.user import AdminUser
from ai_tools_app.core.config import settings 
from upload_file_doc import  download_file, upload_image, upload_image_to_firebase
app = FastAPI(title="Rockstar API")
from datetime import datetime
# security = HTTPBasic()


"""Template App
"""
from typing import Awaitable, Callable

from fastapi import FastAPI
# import firebase_admin
# from firebase_admin import credentials


# def register_startup_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
#     """Actions to run on app startup.

#     This function uses fastAPI app to store data
#     inthe state, such as db_engine.

#     :param app: the fastAPI app.
#     :return: function that actually performs actions.
#     """

#     @app.on_event('startup')
#     async def _startup() -> None:
#         # cred = credentials.Certificate("/path/to/cred/file")
#         # firebase_admin.initialize_app()
#         pass
#     return _startup


# def register_shutdown_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
#     """Actions to run on app's shutdown.

#     :param app: fastAPI app.
#     :return: function that actually performs actions.
#     """

#     @app.on_event("shutdown")
#     async def _shutdown() -> None:
#         pass

#     return _shutdown
# Define SQLModel classes
class AiTool(SQLModel,table=True):
    __tablename__ = "aitool"
    id: Optional[int] = Field(default=None, primary_key=True)
    result: str
    user_email: str
    company_name: str
    name: str
    main_category: str
    company_URL: str
    linkedin_URL: str
    category: str
    message: str
    twitter_URL: str
    pricing: str
    image: str
    company_description: str
    referrenceId:str
    # category_id: str
class AiAdmin(SQLModel,table=True):
    __table__="ai_admin"
    id:Optional[int]= Field(default=None, primary_key=True)
    email:str
    password:str
class AiToolModel(BaseModel):
    # id: Optional[int] = Field(default=None, primary_key=True)
    result: str="string"
    user_email: str="string"
    company_name: str="string"
    name: str="string"
    main_category: str="string"
    company_URL: str="string"
    linkedin_URL: str="string"
    category: str="string"
    message: str="string"
    twitter_URL: str="string"
    pricing: str="string"
    image: str="string"
    company_description: str="string"
    referrenceId:str="string"
    img: UploadFile=None
    # class Config:
    #     from_attributes = True
    #     populate_by_name = True
    #     arbitrary_types_allowed = False 
class AiToolModelUpdate(BaseModel):
    # id: Optional[int] = Field(default=None, primary_key=True)
    result: str=None
    user_email: str=None
    company_name: str=None
    name: str=None
    main_category: str=None
    company_URL: str=None
    linkedin_URL: str=None
    category: str=None
    message: str=None
    twitter_URL: str=None
    pricing: str=None
    image: str=None
    company_description: str=None
    referrenceId:str=None
    img: UploadFile=None        
# SQLite Database URL
# SQLModel setup
DATABASE_URL =settings.POSTGRES_URL# "sqlite:///./t.db"
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

 

# Database models
# class Category(SQLModel):
#     id: int
#     name: str
#     items: List["Item"] = []

#     class Config:
#         orm_mode = True


# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session

templates=Jinja2Templates(directory='templates')
@app.get('/')
def chat(request: Request):
    return templates.TemplateResponse(
        "index.html",{"request": request}
    )
@app.get("/aitools/all/", response_model=List[AiTool])
async def all_tools(session: Session = Depends(get_session)):
    return session.exec(select(AiTool)).all()


# @app.get('/export')
# def export_fireabse_json(session: Session = Depends(get_session)):
    aitools=[]
    index=1
    with open('backup.json', "r") as file:
        json_data = json.load(file)
    for key,item_data in json_data['__collections__']['category'].items():
        
        session.add(AiTool(            
            result=item_data["result"] or "",
            user_email=item_data["user_email"] or "",
            company_name=item_data["company_name"] or "",
            name=item_data["name"] or "",
            main_category=item_data["main_category"] or "",
            company_URL=item_data["company_URL"] or "",
            linkedin_URL=item_data["linkedin_URL"] or "",
            category=item_data["category"] or "",
            message=item_data["message" ] or "",
            twitter_URL=item_data["twitter_URL"] or "" ,
            pricing=item_data["pricing"] or "",
            image=item_data["image"] or "",
            company_description=item_data["company_description"] or "",
           referrenceId=key
            ))
       
 
         
    session.commit()
    # session.refresh(aitools)    

    return session.exec(select(AiTool)).all()

@app.get("/aitools/{item_id}", response_model=AiTool)
async def get_tools_by_id(item_id: int, session: Session = Depends(get_session)):
    item = session.get(AiTool, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
# CRUD operations
@app.post("/aitools/create",  )
async def create_item(item:AiToolModel=Depends(AiToolModel), session: Session = Depends(get_session),
                     # current_user:AdminUser=Depends(get_current_user_from_bearer),
                      ):
    print(item)
    image_url=None
    if item.img: 
        try: 
         image_url=await upload_image(item.img) 

        except HTTPException as e:
            return f"{e}"
        
        
        item.image=image_url['image_url']
 
    session.add(item)
    session.commit()
    session.refresh(item)
    return item 





@app.put("/aitools/{item_id}", response_model=AiTool)
async def update_tool(item_id: int, item: AiToolModelUpdate=Depends(AiToolModelUpdate), session: Session = Depends(get_session), 
                      #current_user:AdminUser=Depends(get_current_user_from_bearer)
                      ):
    
    db_item = session.get(AiTool, item_id)
    print(db_item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    data=item.dict()
    print(data)
    if item.img:
        del data['img'] 
        try: 
         image_url=await upload_image(item.img) 

        except HTTPException as e:
            return f"{e}"
        print(image_url)
        
        data['image']=image_url['image_url']

    
    # Filter out keys where the value is None
    filtered_dict = {key: value for key, value in data.items() if value is not None}
    print(filtered_dict)
 
    for var_name, value in filtered_dict.items():
        print(var_name)
        print(value)
        setattr(db_item, var_name, value)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@app.delete("/aitools/{item_id}")
async def delete_tool(item_id: int, session: Session = Depends(get_session),
                    #   current_user:AdminUser=Depends(get_current_user_from_bearer)
                       ):
    item = session.get(AiTool, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"message": "Item deleted successfully"}


@app.delete('/deleteall')
def deleteall(session:Session=Depends(get_session),#current_user:AdminUser=Depends(get_current_user_from_bearer)
              ):
    data=session.exec(select(AiTool)).all()
    for item in data:
        session.delete(item)
    session.commit()
    return {"message": "Items deleted successfully"}


# @app.get("/users/me")
# def read_current_user(username: Annotated[str, Depends(get_current_user_from_bearer)]):
#     return {"username": username}

# @app.on_event("startup")
# async def on_startup():  
#     print("start up complete")



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000,reload=True)