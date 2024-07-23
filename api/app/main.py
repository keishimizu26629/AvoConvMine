from fastapi import FastAPI
from routes import user_routes, conversation_routes
from database import Engine, BaseModel as SQLAlchemyBaseModel

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(conversation_routes.router)

@app.on_event("startup")
async def startup():
    SQLAlchemyBaseModel.metadata.create_all(bind=Engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
