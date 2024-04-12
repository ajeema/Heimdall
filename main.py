from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import os
import threading
from src.Configuration.config import Config
from src.LoggingService.logger import Logger
from src.ProjectManagement.project import ProjectManager
from src.StateManagement.state import AgentState
from src.agents.central_agent import Agent
from src.ModelInference.llm import LLM
import tiktoken

# Initialize FastAPI
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request bodies
class ProjectName(BaseModel):
    project_name: str


class MessageData(BaseModel):
    project_name: str
    message: str


class CodeData(BaseModel):
    project_name: str
    code: str


class PromptData(BaseModel):
    prompt: str


# Dependency injections
def get_logger():
    return Logger()


def get_manager():
    return ProjectManager()


def get_config():
    return Config()


TIKTOKEN_ENC = tiktoken.get_encoding("cl100k_base")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
