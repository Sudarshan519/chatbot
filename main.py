import json
from fastapi import FastAPI, File, HTTPException, Depends, Request, UploadFile
from typing import Annotated, Dict, List, Optional
from fastapi.security import HTTPBasic
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.routing import APIRouter

from ai_tools_app.get_user import get_current_username,get_current_user_from_bearer
from ai_tools_app.models.user import AdminUser
from ai_tools_app.core.config import settings
app = FastAPI()

security = HTTPBasic()


"""Template App
"""
from typing import Awaitable, Callable

from fastapi import FastAPI
import firebase_admin
# from firebase_admin import credentials


def register_startup_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """Actions to run on app startup.

    This function uses fastAPI app to store data
    inthe state, such as db_engine.

    :param app: the fastAPI app.
    :return: function that actually performs actions.
    """

    @app.on_event('startup')
    async def _startup() -> None:
        # cred = credentials.Certificate("/path/to/cred/file")
        firebase_admin.initialize_app()
    return _startup


def register_shutdown_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """Actions to run on app's shutdown.

    :param app: fastAPI app.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        pass

    return _shutdown
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
    

    class Config:
        orm_mode = True
        
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

templates=Jinja2Templates(directory='')
@app.get('/')
def chat(request: Request):
    return templates.TemplateResponse(
        "index.html",{"request": request}
    )
@app.get("/aitools/all/", response_model=List[AiTool])
async def all_tools(session: Session = Depends(get_session)):
    return session.exec(select(AiTool)).all()


@app.get('/export')
def export_fireabse_json(session: Session = Depends(get_session)):
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
@app.post("/aitools/", response_model=AiTool,)
async def create_item(item: AiTool,image:UploadFile =File(...), session: Session = Depends(get_session),
                     # current_user:AdminUser=Depends(get_current_user_from_bearer),
                      ):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item





@app.put("/aitools/{item_id}", response_model=AiTool)
async def update_tool(item_id: int, item: AiTool, session: Session = Depends(get_session), 
                      #current_user:AdminUser=Depends(get_current_user_from_bearer)
                      ):
    db_item = session.get(AiTool, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for var_name, value in vars(item).items():
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


@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_user_from_bearer)]):
    return {"username": username}