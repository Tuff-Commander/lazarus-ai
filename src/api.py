from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse  # <--- NEW IMPORT
from pydantic import BaseModel
from pathlib import Path
import shutil
import os

# --- IMPORTS ---
from src.scanner import scan_repository
from src.dependency_manager import update_dependencies
from src.security_patcher import patch_security
from src.code_modernizer import modernize_codebase

app = FastAPI(title="Lazarus AI API", description="Resurrection Engine Backend")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class RepoRequest(BaseModel):
    url: str

class ResurrectionRequest(BaseModel):
    local_path: str
    details: list

# --- ENDPOINTS ---
@app.get("/")
def health_check():
    return {"status": "online", "message": "Lazarus Engine is Hunting."}

@app.post("/scan")
def scan_endpoint(request: RepoRequest):
    try:
        report = scan_repository(request.url, cleanup=False)
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/resurrect")
def resurrect_endpoint(request: ResurrectionRequest):
    path = request.local_path
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Repository ghost not found.")

    try:
        dep_results = update_dependencies(path, request.details)
        sec_results = patch_security(path)
        mod_results = modernize_codebase(path)
        
        return {
            "status": "Resurrection Complete",
            "results": {
                "dependencies": dep_results,
                "security": sec_results,
                "modernization": mod_results
            },
            "local_path": path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- UPDATED DOWNLOAD ENDPOINT ---
@app.get("/download/{project_name}")
def download_endpoint(project_name: str, local_path: str):
    try:
        # Sanitize name
        safe_name = "".join([c for c in project_name if c.isalnum() or c in (' ', '-', '_')]).strip()
        
        # Create Zip
        zip_path = shutil.make_archive(
            str(Path(local_path).parent / f"lazarus_{safe_name}"), 
            'zip', 
            local_path
        )
        
        # Return the actual file stream (Browser will treat this as a download)
        return FileResponse(
            path=zip_path, 
            filename=f"lazarus_{safe_name}.zip", 
            media_type='application/zip'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))