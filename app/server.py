
from uuid import uuid4
from urllib.parse import urlparse

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

from app.services.git_service import clone_repository
from app.services.repository_inventory import create_repository_inventory
from app.services.document_loader import load_repository_documents
from app.services.text_splitter import split_documents

app = FastAPI(
    title="RepoLens API",
    description="AI-powered GitHub repository analyzer",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
  allow_origins=[
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5173",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Temporary in-memory storage for the MVP.
JOBS = {}


class AnalysisRequest(BaseModel):
    repo_url: HttpUrl

def run_analysis(analysis_id: str, repo_url: str):
    try:
        JOBS[analysis_id]["status"] = "running"
        JOBS[analysis_id]["progress"] = 10
        JOBS[analysis_id]["message"] = "Cloning repository"

        # STEP 1: Clone repository
        repo_path = clone_repository(repo_url)

        JOBS[analysis_id]["progress"] = 30
        JOBS[analysis_id]["message"] = "Creating repository inventory"

        # STEP 2: Create inventory
        inventory = create_repository_inventory(repo_path)

        JOBS[analysis_id]["progress"] = 50
        JOBS[analysis_id]["message"] = "Loading repository documents"

        # STEP 3: Load documents
        documents = load_repository_documents(repo_path)

        JOBS[analysis_id]["progress"] = 70
        JOBS[analysis_id]["message"] = "Splitting documents into chunks"

        # STEP 4: Split documents
        chunks = split_documents(documents)

        # STEP 4: Verify chunking results
        print("\n========== CHUNKING RESULTS ==========")

        print("Documents loaded:", len(documents))
        print("Total chunks created:", len(chunks))

        for chunk in chunks[:5]:
            print("\n-----------------------------")
            print("Source:", chunk.metadata.get("source"))
            print("Chunk index:", chunk.metadata.get("chunk_index"))
            print("Start index:", chunk.metadata.get("start_index"))
            print("Characters:", len(chunk.page_content))
            print("Preview:", chunk.page_content[:200])

            print("=====================================\n")

        # Keep documents and chunks in memory
        JOBS[analysis_id]["documents"] = documents
        JOBS[analysis_id]["chunks"] = chunks

        JOBS[analysis_id]["progress"] = 100
        JOBS[analysis_id]["status"] = "completed"
        JOBS[analysis_id]["message"] = "Document chunking completed"

        JOBS[analysis_id]["result"] = {
            "repository": repo_url,
            "inventory": inventory,
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
            "document_sources": [
                doc.metadata["source"] for doc in documents
            ],
            "chunk_sources": [
                {
                    "source": chunk.metadata["source"],
                    "chunk_index": chunk.metadata["chunk_index"],
                    "start_index": chunk.metadata.get("start_index"),
                }
                for chunk in chunks
            ],
        }

    except Exception as error:
        JOBS[analysis_id]["status"] = "failed"
        JOBS[analysis_id]["message"] = str(error)


@app.get("/")
def health_check():
    return {"message": "RepoLens API is running"}


@app.post("/api/analyses", status_code=202)
def create_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
):
    parsed_url = urlparse(str(request.repo_url))

    if parsed_url.hostname != "github.com":
        raise HTTPException(
            status_code=400,
            detail="Only GitHub repository URLs are supported",
        )

    parts = parsed_url.path.strip("/").split("/")

    if len(parts) != 2 or not all(parts):
        raise HTTPException(
            status_code=400,
            detail="Provide a valid GitHub owner/repository URL",
        )

    analysis_id = str(uuid4())

    JOBS[analysis_id] = {
        "status": "queued",
        "progress": 0,
        "message": "Waiting to start",
        "result": None,
    }

    background_tasks.add_task(
        run_analysis,
        analysis_id,
        str(request.repo_url),
    )

    return {
        "analysis_id": analysis_id,
        "status": "queued",
    }


@app.get("/api/analyses/{analysis_id}")
def get_analysis_status(analysis_id: str):
    job = JOBS.get(analysis_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    return {
        "analysis_id": analysis_id,
        "status": job["status"],
        "progress": job["progress"],
        "message": job["message"],
    }


@app.get("/api/analyses/{analysis_id}/report")
def get_analysis_report(analysis_id: str):
    job = JOBS.get(analysis_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    if job["status"] != "completed":
        raise HTTPException(
            status_code=409,
            detail="Analysis is not completed yet",
        )

    return job["result"]
