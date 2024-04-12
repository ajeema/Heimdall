from fastapi import FastAPI, Depends, HTTPException, FileResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

# Assuming logger, project manager, and config classes are implemented elsewhere and imported here
from src.LoggingService.logger import Logger
from src.Configuration.config import Config
from src.ProjectManagement.project import ProjectManager
from src.StateManagement.state import AgentState

app = FastAPI()

# Dependency injector functions
def get_logger():
    return Logger()

def get_manager():
    return ProjectManager()

def get_config():
    return Config()

# Pydantic model for data validation
class ProjectName(BaseModel):
    project_name: str

@app.post("/api/create-project")
async def create_project(project: ProjectName, logger: Logger = Depends(get_logger), manager: ProjectManager = Depends(get_manager)):
    """
    Create a new project with the given name.
    """
    manager.create_project(project.project_name)
    logger.log(f"Project created: {project.project_name}")
    return {"message": "Project created"}

@app.post("/api/delete-project")
async def delete_project(project: ProjectName, logger: Logger = Depends(get_logger), manager: ProjectManager = Depends(get_manager)):
    """
    Delete an existing project and its associated state.
    """
    manager.delete_project(project.project_name)
    AgentState().delete_state(project.project_name)
    logger.log(f"Project deleted: {project.project_name}")
    return {"message": "Project deleted"}

@app.get("/api/download-project/{project_name}")
async def download_project(project_name: str, manager: ProjectManager = Depends(get_manager)):
    """
    Download a project as a zip file.
    """
    project_path = manager.get_zip_path(project_name)
    return FileResponse(project_path, media_type='application/octet-stream', filename=f"{project_name}.zip")

@app.get("/api/download-project-pdf/{project_name}")
async def download_project_pdf(project_name: str, config: Config = Depends(get_config)):
    """
    Download a PDF document associated with the project.
    """
    try:
        pdf_dir = config.get_pdfs_dir()
        pdf_path = os.path.join(pdf_dir, f"{project_name}.pdf")
        return FileResponse(pdf_path, media_type='application/pdf')
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="PDF file not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


