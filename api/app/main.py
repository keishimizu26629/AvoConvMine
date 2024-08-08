from fastapi import FastAPI
from routes import user_routes, conversation_routes, friend_routes, chat_routes, auth_routes, test_routes
from database import Engine, BaseModel as SQLAlchemyBaseModel

app = FastAPI()

app.include_router(test_routes.router, prefix="/test", tags=["test"])
app.include_router(auth_routes.router, prefix="/auth", tags=["authentication"])
app.include_router(user_routes.router)
app.include_router(conversation_routes.router)
app.include_router(friend_routes.router)
app.include_router(chat_routes.router)

@app.on_event("startup")
async def startup():
    SQLAlchemyBaseModel.metadata.create_all(bind=Engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
