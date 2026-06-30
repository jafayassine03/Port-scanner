const fileInput = document.getElementById("fileInput");
const searchBox = document.getElementById("searchBox");
const logsDiv = document.getElementById("logs");

const totalLogs = document.getElementById("totalLogs");
const infoCount = document.getElementById("infoCount");
const warningCount = document.getElementById("warningCount");
const errorCount = document.getElementById("errorCount");
const criticalCount = document.getElementById("criticalCount");

const showAll = document.getElementById("showAll");
const showInfo = document.getElementById("showInfo");
const showWarnings = document.getElementById("showWarnings");
const showErrors = document.getElementById("showErrors");
const showCritical = document.getElementById("showCritical");

const exportLogs = document.getElementById("exportLogs");
const toggleTheme = document.getElementById("toggleTheme");
const clearLogs = document.getElementById("clearLogs");

let allLogs = [];
let currentFilter = "ALL";
let chart;

function getLogType(line) {
    const upper = line.toUpperCase();

    if (upper.includes("CRITICAL")) return "CRITICAL";
    if (upper.includes("ERROR")) return "ERROR";
    if (upper.includes("WARNING")) return "WARNING";
    if (upper.includes("INFO")) return "INFO";

    return "OTHER";
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function displayLogs(lines) {
    logsDiv.innerHTML = "";

    if (!lines.length) {
        logsDiv.innerHTML = `
            <div class="empty-state">
                No matching log entries found.
            </div>
        `;
        return;
    }

    lines.forEach((line, index) => {
        const div = document.createElement("div");

        div.classList.add("log-entry");

        const type = getLogType(line);

        if (type === "INFO") div.classList.add("info");
        if (type === "WARNING") div.classList.add("warning");
        if (type === "ERROR") div.classList.add("error");
        if (type === "CRITICAL") div.classList.add("critical");

        div.innerHTML = `
            <span class="line-number">#${index + 1}</span>
            <span class="log-text">${escapeHtml(line)}</span>
        `;

        div.title = "Click to copy";

        div.addEventListener("click", () => {
            navigator.clipboard.writeText(line);

            div.classList.add("copied");

            setTimeout(() => {
                div.classList.remove("copied");
            }, 500);
        });

        logsDiv.appendChild(div);
    });
}

function updateStats(lines) {
    let info = 0;
    let warning = 0;
    let error = 0;
    let critical = 0;

    const duplicates = new Set();
    const seen = new Set();

    lines.forEach(line => {
        const type = getLogType(line);

        if (type === "INFO") info++;
        if (type === "WARNING") warning++;
        if (type === "ERROR") error++;
        if (type === "CRITICAL") critical++;

        if (seen.has(line)) {
            duplicates.add(line);
        }

        seen.add(line);
    });

    totalLogs.textContent = lines.length;
    infoCount.textContent = info;
    warningCount.textContent = warning;
    errorCount.textContent = error;

    if (criticalCount) {
        criticalCount.textContent = critical;
    }

    const duplicateCounter = document.getElementById("duplicateCount");

    if (duplicateCounter) {
        duplicateCounter.textContent = duplicates.size;
    }
}

function updateChart(lines) {
    const canvas = document.getElementById("logChart");

    if (!canvas || typeof Chart === "undefined") return;

    let info = 0;
    let warning = 0;
    let error = 0;
    let critical = 0;

    lines.forEach(line => {
        const type = getLogType(line);

        if (type === "INFO") info++;
        if (type === "WARNING") warning++;
        if (type === "ERROR") error++;
        if (type === "CRITICAL") critical++;
    });

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(canvas, {
        type: "bar",
        data: {
            labels: ["INFO", "WARNING", "ERROR", "CRITICAL"],
            datasets: [{
                data: [info, warning, error, critical]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function applyFilters() {
    const search = searchBox.value.toLowerCase();

    let filtered = [...allLogs];

    if (currentFilter !== "ALL") {
        filtered = filtered.filter(line =>
            getLogType(line) === currentFilter
        );
    }

    if (search) {
        filtered = filtered.filter(line =>
            line.toLowerCase().includes(search)
        );
    }

    displayLogs(filtered);
    updateStats(filtered);
    updateChart(filtered);
}

fileInput.addEventListener("change", function () {
    const file = this.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = e => {
        allLogs = e.target.result
            .split(/\r?\n/)
            .filter(line => line.trim());

        applyFilters();
    };

    reader.readAsText(file);
});

searchBox.addEventListener("input", applyFilters);

showAll.addEventListener("click", () => {
    currentFilter = "ALL";
    applyFilters();
});

showInfo.addEventListener("click", () => {
    currentFilter = "INFO";
    applyFilters();
});

showWarnings.addEventListener("click", () => {
    currentFilter = "WARNING";
    applyFilters();
});

showErrors.addEventListener("click", () => {
    currentFilter = "ERROR";
    applyFilters();
});

if (showCritical) {
    showCritical.addEventListener("click", () => {
        currentFilter = "CRITICAL";
        applyFilters();
    });
}

exportLogs.addEventListener("click", () => {
    const text = Array.from(
        document.querySelectorAll(".log-text")
    )
        .map(el => el.textContent)
        .join("\n");

    if (!text.trim()) return;

    const blob = new Blob(
        [text],
        { type: "text/plain" }
    );

    const a = document.createElement("a");

    a.href = URL.createObjectURL(blob);
    a.download = "filtered_logs.txt";

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(a.href);
});

if (toggleTheme) {
    toggleTheme.addEventListener("click", () => {
        document.body.classList.toggle("light-mode");

        if (document.body.classList.contains("light-mode")) {
            toggleTheme.textContent = "☀️ Light Mode";
        } else {
            toggleTheme.textContent = "🌙 Dark Mode";
        }
    });
}

if (clearLogs) {
    clearLogs.addEventListener("click", () => {
        allLogs = [];
        currentFilter = "ALL";

        logsDiv.innerHTML =
            "Upload a log file to begin analysis.";

        totalLogs.textContent = "0";
        infoCount.textContent = "0";
        warningCount.textContent = "0";
        errorCount.textContent = "0";

        if (criticalCount) {
            criticalCount.textContent = "0";
        }

        searchBox.value = "";

        if (chart) {
            chart.destroy();
            chart = null;
        }
    });
}