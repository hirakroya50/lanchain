
from uuid import uuid4
from urllib.parse import urlparse

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

from app.services.git_service import clone_repository
from app.services.repository_inventory import create_repository_inventory
from app.services.document_loader import load_repository_documents
from app.services.text_splitter import split_documents
from app.services.llm_analyzer import analyze_chunk
from app.services.report_generator import generate_project_report
from app.schemas.analysis_request import AnalysisRequest
from app.schemas.analysis_response import AnalysisCreatedResponse
import uuid
from fastapi import BackgroundTasks
from app.schemas.job_status import JobStatus
from app.schemas.report import RepositoryReport

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

        JOBS[analysis_id]["progress"] = 25
        JOBS[analysis_id]["message"] = "Creating repository inventory"

        # STEP 2: Create inventory
        inventory = create_repository_inventory(repo_path)

        JOBS[analysis_id]["progress"] = 40
        JOBS[analysis_id]["message"] = "Loading repository documents"

        # STEP 3: Load documents
        documents = load_repository_documents(repo_path)

        if not documents:
            raise ValueError("No supported documents found in repository")

        JOBS[analysis_id]["progress"] = 50
        JOBS[analysis_id]["message"] = "Splitting documents into chunks"

        # STEP 4: Split documents
        chunks = split_documents(documents)

        if not chunks:
            raise ValueError("No chunks were generated from repository documents")

        # Keep documents and chunks in memory
        JOBS[analysis_id]["documents"] = documents
        JOBS[analysis_id]["chunks"] = chunks

        # STEP 5: Display chunking information
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

        # STEP 6: Analyze repository chunks using LLM

        JOBS[analysis_id]["progress"] = 55
        JOBS[analysis_id]["message"] = "Starting AI chunk analysis"

        # Limit API usage during development
        MAX_CHUNKS_PER_ANALYSIS = 5
        chunks_to_analyze = chunks[:MAX_CHUNKS_PER_ANALYSIS]

        # Convert HttpUrl into a regular Python string
        repo_url = str(repo_url)

        # Extract repository name
        project_name = repo_url.rstrip("/").split("/")[-1]
        project_name = project_name.removesuffix(".git")

        chunk_analyses = []

        for index, chunk in enumerate(chunks_to_analyze):

            file_path = chunk.metadata.get("source", "unknown")

            JOBS[analysis_id]["message"] = (
                f"Analyzing chunk {index + 1}/{len(chunks_to_analyze)}: "
                f"{file_path}"
            )

            analysis = analyze_chunk(
                project_name=project_name,
                file_path=file_path,
                code=chunk.page_content,
            )

            analysis_data = analysis.model_dump()

            analysis_data["file_path"] = file_path
            analysis_data["chunk_index"] = chunk.metadata["chunk_index"]

            chunk_analyses.append(analysis_data)

            # Progress: 55% to 85%
            progress = 55 + int(
                ((index + 1) / len(chunks_to_analyze)) * 30
            )

            JOBS[analysis_id]["progress"] = progress

        JOBS[analysis_id]["chunk_analyses"] = chunk_analyses

        # STEP 7: Generate consolidated project report

        JOBS[analysis_id]["progress"] = 90
        JOBS[analysis_id]["message"] = "Generating project report"

        report = generate_project_report(
            project_name=project_name,
            chunk_analyses=chunk_analyses,
        )

        # Convert Pydantic report into a dictionary
        report_data = report.model_dump()

        JOBS[analysis_id]["report"] = report_data

        # STEP 8: Store final results

        JOBS[analysis_id]["progress"] = 98
        JOBS[analysis_id]["message"] = "Saving analysis results"

        JOBS[analysis_id]["result"] = {
            "repository": repo_url,
            "inventory": inventory,
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
            "chunks_analyzed": len(chunk_analyses),
            "chunk_analyses": chunk_analyses,
            "project_report": report_data,

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

        # STEP 9: Mark analysis as completed

        JOBS[analysis_id]["progress"] = 100
        JOBS[analysis_id]["status"] = "completed"
        JOBS[analysis_id]["message"] = "Project analysis completed successfully"

        print("\n========== PROJECT REPORT ==========")
        print(report.model_dump_json(indent=2))
        print("====================================\n")
    
    except Exception as error:

        import traceback

        JOBS[analysis_id]["status"] = "failed"
        JOBS[analysis_id]["progress"] = 0
        JOBS[analysis_id]["message"] = "Analysis failed"
        JOBS[analysis_id]["error"] = str(error)

        print("\n========== ANALYSIS ERROR ==========")
        print(f"Error: {error}")
        traceback.print_exc()
        print("====================================\n")




        

@app.get("/")
def health_check():
    return {"message": "RepoLens API is running"}


@app.post(
    "/api/analyses",
    response_model=AnalysisCreatedResponse
)
def create_analysis(
    data: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    analysis_id = str(uuid.uuid4())

    JOBS[analysis_id] = {
        "status": "pending",
        "progress": 0,
        "message": "Analysis queued",
        "result": None,
        "error": None,
    }

    background_tasks.add_task(
        run_analysis,
        analysis_id,
        data.repo_url,
    )

    return AnalysisCreatedResponse(
        analysis_id=analysis_id,
        status="pending",
        message="Repository analysis started",
    )


def create_analysis(
    data: AnalysisRequest,
    background_tasks: BackgroundTasks
):

    analysis_id = str(uuid.uuid4())

    JOBS[analysis_id] = {
        "status": "pending",
        "progress": 0,
        "message": "Analysis queued",
        "result": None,
        "error": None,
    }

    background_tasks.add_task(
        run_analysis,
        analysis_id,
        data.repo_url,
    )

    return AnalysisCreatedResponse(
        analysis_id=analysis_id,
        status="pending",
        message="Repository analysis started",
    )



@app.get(
    "/api/analyses/{analysis_id}",
    response_model=JobStatus
)
def get_analysis_status(analysis_id: str):

    # Step 1: Find the analysis job
    job = JOBS.get(analysis_id)

    # Step 2: Check whether the job exists
    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    # Step 3: Build the response
    response = JobStatus(
        analysis_id=analysis_id,
        status=job.get("status", "pending"),
        progress=job.get("progress", 0),
        message=job.get("message", ""),
        error=job.get("error"),
    )

    # Step 4: Return validated response
    return response


@app.get("/api/analyses/{analysis_id}/report")
def get_analysis_report(analysis_id: str):

    # 1. Find the analysis job
    job = JOBS.get(analysis_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    # 2. Check analysis status
    if job.get("status") == "failed":
        raise HTTPException(
            status_code=409,
            detail=job.get("error", "Analysis failed"),
        )

    if job.get("status") != "completed":
        raise HTTPException(
            status_code=409,
            detail="Analysis is not completed yet",
        )

    # 3. Get complete analysis result
    result = job.get("result")

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Analysis result not found",
        )

    # 4. Return inventory + AI report + analysis metadata
    return result
