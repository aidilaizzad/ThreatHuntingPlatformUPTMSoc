document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded!"); // ✅ Debugging step
    refreshLogs();
    setInterval(refreshLogs, 5000); // Auto-refresh logs every 5 seconds
});

// ✅ Fetch Logs & Update Table & Graph
function refreshLogs() {
    console.log("Fetching logs..."); // ✅ Debugging step
    fetch('/logs')
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to fetch logs.");
        }
        return response.json();
    })
    .then(logs => {
        console.log("Logs received:", logs); // ✅ Debugging step
        updateLogs(logs);
        updateGraph();
    })
    .catch(error => console.error("Error fetching logs:", error));
}

// ✅ Fix Form Submission
document.getElementById("log-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const message = document.getElementById("log-message").value;
    const value = parseFloat(document.getElementById("log-value").value);

    if (!message || isNaN(value)) {
        alert("Please enter a valid message and value.");
        return;
    }

    console.log("Submitting Log:", message, value); // ✅ Debugging step

    fetch("/add_log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message, value: value }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Log added successfully:", data); // ✅ Debugging step
        alert("Log added!");
        document.getElementById("log-form").reset(); // ✅ Clear form after submit
        refreshLogs(); // ✅ Reload logs
    })
    .catch(error => console.error("Error adding log:", error));
});

// ✅ Update Table with Logs
function updateLogs(logs) {
    console.log("Updating logs table..."); // ✅ Debugging step
    const logsContainer = document.getElementById('logsContainer');
    if (!logsContainer) {
        console.error("Logs container element not found!");
        return;
    }
    logsContainer.innerHTML = ''; // Clear old logs before updating

    logs.forEach(log => {
        console.log("Adding log:", log); // ✅ Debugging step

        const logElement = document.createElement('tr');
        logElement.classList.add("log-entry");
        logElement.innerHTML = `
            <td>${log.timestamp}</td>
            <td class="log-message">${escapeString(log.message)}</td>
            <td>${log.value}</td>
            <td>${log.status}</td>
            <td>${log.threat_type}</td> <!-- ✅ Display Threat Type -->
	    <td>${log.severity}</td>
            <td><button class="delete-btn" onclick="removeLog(${log.id})">Delete</button></td>
        `;
        logsContainer.appendChild(logElement);
    });

    console.log("Logs successfully added to table."); // ✅ Debugging step
}

// ✅ Refresh Graph (Solution 1: Auto-refresh)
function updateGraph() {
    const graphElement = document.getElementById("logGraph");
    if (graphElement) {
        graphElement.src = `/static/graph.png?t=${new Date().getTime()}`; // ✅ Auto-refresh graph
    } else {
        console.error("Graph element not found!");
    }
}

// ✅ Escape Special Characters (Fix Regex Errors)
function escapeString(str) {
    if (typeof str !== "string") return str; // Ensure it's a string
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // Proper escaping
}

// ✅ Search Logs (Fix Any Regex Issues)
function searchLogs() {
    const input = document.getElementById("search-input").value.toLowerCase();
    const logs = document.querySelectorAll(".log-entry");

    logs.forEach(log => {
        const message = log.querySelector(".log-message").textContent.toLowerCase();
        log.style.display = message.includes(input) ? "" : "none";
    });
}

// ✅ Remove Log (Fixed Syntax)
function removeLog(logId) {
    fetch(`/remove_log/${logId}`, { method: "DELETE" }) // ✅ FIXED Backticks
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to delete log.");
        }
        return response.json();
    })
    .then(data => {
        console.log("Log deleted successfully:", data); // ✅ Debugging step
        alert(data.message);
        refreshLogs();
    })
    .catch(error => console.error("Error removing log:", error));
}

// ✅ Refresh Graph (Ensures Graph Updates)
function updateGraph() {
    const graphElement = document.getElementById("logGraph");
    if (graphElement) {
        graphElement.src = `/static/graph.png?t=${new Date().getTime()}`; // ✅ FIXED Backticks
    } else {
        console.error("Graph element not found!");
    }
}
fetch("/add_log", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        message: "Unauthorized login attempt",
        value: 500,
        action: "Block User"  // ✅ Ensure this is sent
    })
})
.then(response => response.json())
.then(data => console.log("Response:", data));
