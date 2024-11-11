from typing import Union, Optional, TypeAlias, List, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import Field, SQLModel, create_engine, Session, text, insert, Table, Column, String, Text, Integer
# from sqlalchemy import text
from pydantic import BaseModel
from contextlib import asynccontextmanager

import random

class Story(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine("postgresql://postgres:postgres@db:5432/postgres")

async def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/stories/", response_model=Story)
def create_story(story: Story):
    with Session(engine) as session:
        session.add(story)
        session.commit()
        session.refresh(story)

    addEmbedding(story.title, story.content)
    return story

def addEmbedding(title: str, content:str):
    with engine.connect() as conn:
        embed_statement = "select ai.ollama_embed( 'llama3.2', :content, host=>'http://host.docker.internal:11434')"
        embedding = conn.execute(text(embed_statement), {"content": content}).mappings().first()
        if embedding:
            result = conn.execute(text("INSERT INTO story_embeddings (title, content, embedding) VALUES (:title, :content, :embedding)"), [{"title": title, "content": content, "embedding": embedding['ollama_embed']}])
            conn.commit()
            return result

@app.get("/scifi")
def read_item(topic: str = 'robots'):
    with engine.connect() as conn:
        statement = "select ai.ollama_chat_complete( 'llama3.2', jsonb_build_array ( jsonb_build_object('role', 'system', 'content', 'you are a science fiction writer focused on {topic}.'), jsonb_build_object('role', 'user', 'content', 'Give a title with at least 5 words and a long summary of a novel you will write next.')), chat_options=> jsonb_build_object( 'seed', {seed}, 'temperature', 0.9, 'repeat_penalty', 0.9), host=>'http://host.docker.internal:11434')".format(topic=topic, seed=random.random() * 100)
        result = conn.execute(text(statement)).mappings().all()
    return result

class EditorText(BaseModel):
    editor_text: str

@app.post("/suggestions")
def get_suggestions(editorText: EditorText):
    with engine.connect() as conn:
        statement = "select ai.ollama_chat_complete( 'llama3.2', jsonb_build_array ( jsonb_build_object('role', 'system', 'content', 'you are a science fiction writer. You are provided the starting prompt text of: {editor_text}'), jsonb_build_object('role', 'user', 'content', 'Complete the next few paragraphs given the starting text. Provide a response several paragraphs long.')), chat_options=> jsonb_build_object( 'seed', {seed}, 'temperature', 0.9, 'repeat_penalty', 0.9), host=>'http://host.docker.internal:11434')".format(editor_text=editorText.editor_text, seed=random.random() * 100)
        result = conn.execute(text(statement)).mappings().all()
    return result

@app.get("/stories/")
def get_stories():
     with engine.connect() as conn:
        story_stmt = "select * from story"
        result = conn.execute(text(story_stmt)).mappings().all()
        return result

@app.get("/stories/{story_id}")
def get_story_by_id(story_id: int, q: Union[str, None] = None):
    with engine.connect() as conn:
        story_stmt = "select * from story where id = :story_id"
        result = conn.execute(text(story_stmt), [{ "story_id": story_id}]).mappings().first()
        return result