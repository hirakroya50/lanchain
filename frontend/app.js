
const API_BASE_URL = "http://localhost:8000";

const repoInput = document.getElementById("repoUrl");
const analyzeBtn = document.getElementById("analyzeBtn");

const progressSection = document.getElementById("progressSection");
const resultsSection = document.getElementById("resultsSection");
const errorSection = document.getElementById("errorSection");

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function showError(message) {
    errorSection.classList.remove("hidden");
    document.getElementById("errorMessage").textContent = message;
}

function hideError() {
    errorSection.classList.add("hidden");
}

function setProgress(progress, message) {
    document.getElementById("progressBar").style.width = `${progress}%`;
    document.getElementById("progressPercent").textContent = `${progress}%`;
    document.getElementById("progressMessage").textContent = message;
}

function setLoading(loading) {
    analyzeBtn.disabled = loading;
    analyzeBtn.textContent = loading ? "Analyzing..." : "Analyze Repository ↗";
}

async function checkAPI() {
    const statusText = document.getElementById("apiStatus");
    const dot = document.querySelector(".status-dot");

    try {
        const response = await fetch(`${API_BASE_URL}/`);

        if (!response.ok) throw new Error("API unavailable");

        statusText.textContent = "API Connected";
        dot.classList.add("online");
        dot.classList.remove("offline");
    } catch {
        statusText.textContent = "API Offline";
        dot.classList.add("offline");
        dot.classList.remove("online");
    }
}

async function startAnalysis() {
    const repoUrl = repoInput.value.trim();

    if (!repoUrl) {
        showError("Please enter a GitHub repository URL.");
        return;
    }

    hideError();
    resultsSection.classList.add("hidden");
    progressSection.classList.remove("hidden");
    setLoading(true);
    setProgress(0, "Submitting repository...");

    try {
        // 1. Create analysis job
        const createResponse = await fetch(`${API_BASE_URL}/api/analyses`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                repo_url: repoUrl
            })
        });

        const createData = await createResponse.json();

        if (!createResponse.ok) {
            throw new Error(createData.detail || "Could not start analysis.");
        }

        const analysisId = createData.analysis_id;

        // 2. Poll job status
        let jobCompleted = false;

        while (!jobCompleted) {
            await sleep(1500);

            const statusResponse = await fetch(
                `${API_BASE_URL}/api/analyses/${analysisId}`
            );

            const statusData = await statusResponse.json();

            if (!statusResponse.ok) {
                throw new Error(statusData.detail || "Could not get analysis status.");
            }

            setProgress(
                statusData.progress,
                statusData.message
            );

            if (statusData.status === "completed") {
                jobCompleted = true;
            } else if (statusData.status === "failed") {
                throw new Error(statusData.message || "Analysis failed.");
            }
        }

        // 3. Fetch report
        const reportResponse = await fetch(
            `${API_BASE_URL}/api/analyses/${analysisId}/report`
        );

        const reportData = await reportResponse.json();

        if (!reportResponse.ok) {
            throw new Error(reportData.detail || "Could not retrieve report.");
        }

        // 4. Display report
        displayReport(reportData);

        setProgress(100, "Analysis completed successfully!");
        document.getElementById("progressTitle").textContent = "Analysis completed";

    } catch (error) {
        showError(error.message || "An unexpected error occurred.");
        document.getElementById("progressMessage").textContent = "Analysis failed.";
    } finally {
        setLoading(false);
    }
}

function displayReport(data) {
    const inventory = data.inventory;

    resultsSection.classList.remove("hidden");

    const repoUrl = data.repository || repoInput.value;
    const parts = repoUrl.replace(/\/+$/, "").split("/");

    document.getElementById("repoName").textContent =
        parts[parts.length - 1] || "Repository";

    document.getElementById("repoUrlDisplay").textContent = repoUrl;

    document.getElementById("totalFiles").textContent =
        inventory.total_files;

    document.getElementById("supportedFiles").textContent =
        inventory.supported_files;

    document.getElementById("ignoredFiles").textContent =
        inventory.ignored_files;

    // Extension breakdown
    const extensionList = document.getElementById("extensionList");
    extensionList.replaceChildren();

    const extensions = Object.entries(inventory.extension_counts)
        .sort((a, b) => b[1] - a[1]);

    const maxCount = Math.max(1, ...extensions.map(item => item[1]));

    extensions.forEach(([extension, count]) => {
        const item = document.createElement("div");
        item.className = "extension-item";

        const meta = document.createElement("div");
        meta.className = "extension-meta";

        const name = document.createElement("span");
        name.textContent = extension;

        const amount = document.createElement("span");
        amount.textContent = count;

        meta.append(name, amount);

        const track = document.createElement("div");
        track.className = "extension-track";

        const bar = document.createElement("div");
        bar.className = "extension-bar";
        bar.style.width = `${(count / maxCount) * 100}%`;

        track.append(bar);
        item.append(meta, track);
        extensionList.append(item);
    });

    // Important files
    const importantFiles = document.getElementById("importantFiles");
    importantFiles.replaceChildren();

    if (inventory.important_files.length === 0) {
        const empty = document.createElement("p");
        empty.className = "muted";
        empty.textContent = "No important files detected.";
        importantFiles.append(empty);
    } else {
        inventory.important_files.forEach(file => {
            const item = document.createElement("div");
            item.className = "file-item";
            item.textContent = file.path;
            importantFiles.append(item);
        });
    }

    // Complete file inventory
    const tbody = document.getElementById("fileTableBody");
    tbody.replaceChildren();

    document.getElementById("fileCount").textContent =
        `${inventory.files.length} files`;

    inventory.files.forEach(file => {
        const row = document.createElement("tr");

        const values = [
            file.path,
            file.extension,
            formatBytes(file.size),
            file.is_important ? "Important" : "Source file"
        ];

        values.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.append(cell);
        });

        tbody.append(row);
    });
}

function formatBytes(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

analyzeBtn.addEventListener("click", startAnalysis);

repoInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        startAnalysis();
    }
});

document.getElementById("newAnalysisBtn").addEventListener("click", () => {
    resultsSection.classList.add("hidden");
    progressSection.classList.add("hidden");
    hideError();
    repoInput.value = "";
    repoInput.focus();
    setProgress(0, "Waiting to start...");
    document.getElementById("progressTitle").textContent = "Analyzing repository";
});

checkAPI();
