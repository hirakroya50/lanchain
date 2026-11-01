# RepoLens 🔍

**AI-powered GitHub Repository Analyzer**

RepoLens is a developer tool that analyzes GitHub repositories and generates structured technical insights. It helps developers understand an unfamiliar codebase by examining its file structure, identifying technologies, and progressively building a comprehensive technical report.

The goal is to turn a GitHub repository URL into an understandable overview of the project's architecture, technology stack, code organization, and potential improvements.

## ✨ Features

### Current Features

- **GitHub Repository Analysis** — Submit a public GitHub repository URL for analysis.
- **Repository Cloning** — Clone repositories using GitPython.
- **File Inventory** — Discover and categorize repository files.
- **Technology Discovery** — Identify file extensions and important project configuration files.
- **Analysis Progress** — Track analysis status through the web interface.
- **Structured API Responses** — Expose analysis results through FastAPI.
- **Interactive Dashboard** — View repository statistics and file inventory in a browser.

### Planned Features

- AI-powered project overview and documentation analysis.
- Framework, library, and dependency detection.
- Architecture and module relationship analysis.
- API endpoint discovery.
- Database schema and data-model analysis.
- Test coverage and CI/CD configuration analysis.
- Security and code-quality insights.
- Hybrid RAG retrieval for large repositories.
- Evidence-backed technical recommendations.
- LangGraph-based agentic analysis workflows.

## 🏗️ Architecture

```text
                  ┌──────────────────────┐
                  │    Web Dashboard     │
                  │   HTML / CSS / JS    │
                  └──────────┬───────────┘
                             │
                             │ HTTP / REST
                             ▼
                  ┌──────────────────────┐
                  │      FastAPI         │
                  │     app/server.py    │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Analysis Services   │
                  ├──────────────────────┤
                  │ Git Service          │
                  │ Repository Inventory │
                  │ Document Loader      │
                  │ Text Splitter        │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │    GitHub Repository │
                  └──────────────────────┘

                  AI Analysis Layer
                  ┌──────────────────────┐
                  │       LangChain      │
                  │      OpenRouter      │
                  │   Structured Output  │
                  └──────────────────────┘
```

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Language | Python |
| Backend | FastAPI |
| ASGI Server | Uvicorn |
| LLM Framework | LangChain |
| LLM Provider | OpenRouter |
| LLM Integration | langchain-openai |
| Document Processing | LangChain Text Splitters |
| Data Validation | Pydantic |
| Git Integration | GitPython |
| Environment Variables | python-dotenv |
| Frontend | HTML, CSS, JavaScript |

## 📁 Project Structure

```text
lanchain/
│
├── app/
│   ├── main.py
│   ├── server.py
│   │
│   ├── llm/
│   │   └── client.py
│   │
│   ├── prompts/
│   │   └── analyzer.py
│   │
│   ├── schemas/
│   │   └── report.py
│   │
│   └── services/
│       ├── git_service.py
│       ├── document_loader.py
│       ├── text_splitter.py
│       └── repository_inventory.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.9+
- Git
- pip
- An OpenRouter API key

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd lanchain
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Get your API key from [OpenRouter](https://openrouter.ai/).

**Important:** Never commit your `.env` file or expose your API key in frontend code.

### 5. Start the backend

From the project root:

```bash
uvicorn app.server:app --reload --port 8000
```

Backend API:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

### 6. Start the frontend

Open a second terminal:

```bash
python -m http.server 5500 --directory frontend
```

Open the dashboard:

```text
http://localhost:5500
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend health check |
| POST | `/api/analyses` | Start repository analysis |
| GET | `/api/analyses/{analysis_id}` | Get analysis progress |
| GET | `/api/analyses/{analysis_id}/report` | Retrieve completed analysis |

### Start an analysis

**Request**

```http
POST /api/analyses
Content-Type: application/json
```

```json
{
  "repo_url": "https://github.com/owner/repository"
}
```

**Response**

```json
{
  "analysis_id": "generated-analysis-id",
  "status": "queued"
}
```

### Check analysis progress

```http
GET /api/analyses/{analysis_id}
```

Example response:

```json
{
  "analysis_id": "generated-analysis-id",
  "status": "running",
  "progress": 40,
  "message": "Creating repository inventory"
}
```

### Retrieve the report

```http
GET /api/analyses/{analysis_id}/report
```

The report endpoint returns the repository analysis result after processing is complete.

## 🧠 AI Analysis Approach

RepoLens is being developed around a structured repository-analysis pipeline.

The intended processing stages are:

1. **Repository Discovery** — Clone the repository and inspect its structure.
2. **File Classification** — Identify source files, configuration files, documentation, and tests.
3. **Document Loading** — Extract relevant text from supported files.
4. **Text Splitting** — Divide large documents into manageable chunks.
5. **AI Analysis** — Analyze code and project documentation using an LLM.
6. **Structured Output** — Validate findings using Pydantic schemas.
7. **Report Generation** — Combine findings into a technical report.

For larger repositories, the planned architecture will use hierarchical analysis and RAG rather than sending the entire codebase to an LLM in a single request.

## 🔐 Security Considerations

RepoLens is currently a learning/MVP project. Before exposing it publicly, additional safeguards are required:

- Validate and normalize GitHub repository URLs.
- Restrict clone operations to trusted GitHub hosts.
- Apply repository size, file count, and execution-time limits.
- Never execute scripts or binaries from cloned repositories.
- Exclude secrets and sensitive files from analysis.
- Add API rate limiting and abuse protection.
- Clean up temporary cloned repositories.
- Store API keys only in server-side environment variables.
- Add persistent job storage before using multiple server workers.

## 🗺️ Roadmap

- [x] Initialize Python project.
- [x] Configure LangChain and OpenRouter.
- [x] Implement GitHub repository cloning.
- [x] Implement repository file inventory.
- [x] Implement document loading.
- [x] Implement text splitting.
- [x] Create FastAPI backend.
- [x] Build browser-based dashboard.
- [ ] Integrate AI-powered repository analysis.
- [ ] Generate structured technical reports.
- [ ] Add evidence and source-file references.
- [ ] Implement hierarchical codebase analysis.
- [ ] Add vector database and hybrid retrieval.
- [ ] Implement RAG-based repository question answering.
- [ ] Introduce LangGraph agentic workflows.
- [ ] Add automated testing and production deployment.

## 🎯 Project Goals

RepoLens is designed to explore practical AI engineering concepts, including:

- LLM application development.
- Prompt engineering and structured outputs.
- Repository and document processing.
- RAG and hybrid search.
- Agentic workflows with LangGraph.
- Backend API design.
- Asynchronous processing.
- AI reliability, validation, and security.

The long-term goal is to build a reliable AI engineering tool that can understand, explain, and review real-world software repositories.

## 📄 License

This project is currently intended for learning and development. Add a license file before distributing it publicly.
