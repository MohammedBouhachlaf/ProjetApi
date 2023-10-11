from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    email: str

class Article(BaseModel):
    id: int
    title: str
    content: str


@app.get("/users/{user_id}")
def get_user(user_id: int):
    
    user = {"id": 2, "username": "yohan", "email": "yohan@example.com"}
    return user

@app.post("/users/")
def create_user(user: User):
   
    return user


@app.get("/articles/{article_id}")
def get_article(article_id: int):
    
    
    article= {"id": article_id, "title": "Mon article", "content": "Contenu de l'article."}
    return article

@app.post("/articles/")
def create_article(article: Article):
   
    return article

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
