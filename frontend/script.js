const API_BASE_URL = "http://127.0.0.1:8000";

const form = document.getElementById("evaluate-form");
const resultPlaceholder = document.getElementById("result-placeholder");
const result = document.getElementById("result");

const decisionBadge = document.getElementById("decision-badge");
const threatType = document.getElementById("threat-type");
const severity = document.getElementById("severity");
const action = document.getElementById("action");
const reason = document.getElementById("reason");

const userIdInput = document.getElementById("user_id");
const roleInput = document.getElementById("role");
const methodInput = document.getElementById("method");
const pathInput = document.getElementById("path");
const objectIdInput = document.getElementById("object_id");

const eventsContainer = document.getElementById("events-container");
const refreshEventsButton = document.getElementById("refresh-events");


async function evaluateRequest() {
    const payload = new URLSearchParams();

    payload.append("user_id", userIdInput.value);
    payload.append("role", roleInput.value);
    payload.append("method", methodInput.value);
    payload.append("path", pathInput.value);

    if (objectIdInput.value.trim()) {
        payload.append("object_id", objectIdInput.value.trim());
    }

    const response = await fetch(
        `${API_BASE_URL}/evaluate?${payload.toString()}`,
        {
            method: "POST",
        }
    );

    if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
    }

    return await response.json();
}


function displayResult(data) {
    resultPlaceholder.classList.add("hidden");
    result.classList.remove("hidden");

    decisionBadge.textContent = data.allowed ? "ALLOWED" : "BLOCKED";

    threatType.textContent = data.threat_type || "NONE";
    severity.textContent = data.severity || "NONE";
    action.textContent = data.action || "-";
    reason.textContent = data.reason || "No reason provided.";
}


async function loadEvents() {
    eventsContainer.innerHTML =
        '<p class="events-empty">Loading security events...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/events`);

        if (!response.ok) {
            throw new Error(`Events API failed: ${response.status}`);
        }

        const events = await response.json();

        if (!events.length) {
            eventsContainer.innerHTML =
                '<p class="events-empty">No security events recorded yet.</p>';
            return;
        }

        eventsContainer.innerHTML = events
            .slice()
            .reverse()
            .map((event) => {
                const statusClass = event.allowed
                    ? "event-allowed"
                    : "event-blocked";

                return `
                    <div class="event-row ${statusClass}">
                        <div class="event-main">

                            <div class="event-status">
                                ${event.allowed ? "ALLOWED" : "BLOCKED"}
                            </div>

                            <div class="event-info">
                                <strong>
                                    ${event.method} ${event.path}
                                </strong>

                                <span>
                                    User: ${event.user_id}
                                    · Role: ${event.role}
                                    ${event.object_id
                                        ? ` · Object: ${event.object_id}`
                                        : ""}
                                </span>
                            </div>

                        </div>

                        <div class="event-meta">
                            <span>
                                ${event.threat_type || "NONE"}
                            </span>

                            <span>
                                ${event.severity || "NONE"}
                            </span>

                            <small>
                                ${event.timestamp}
                            </small>
                        </div>
                    </div>
                `;
            })
            .join("");

    } catch (error) {
        eventsContainer.innerHTML =
            '<p class="events-empty">Unable to load security events.</p>';

        console.error(error);
    }
}


form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const button = document.getElementById("evaluate-btn");

    button.disabled = true;
    button.textContent = "Evaluating...";

    try {
        const data = await evaluateRequest();

        displayResult(data);

        await loadEvents();

    } catch (error) {
        resultPlaceholder.classList.add("hidden");
        result.classList.remove("hidden");

        decisionBadge.textContent = "ERROR";
        threatType.textContent = "-";
        severity.textContent = "-";
        action.textContent = "ERROR";

        reason.textContent =
            "Unable to connect to the Security Engine. Make sure the FastAPI server is running.";

        console.error(error);

    } finally {
        button.disabled = false;
        button.textContent = "Evaluate Request";
    }
});


document.querySelectorAll(".quick-test").forEach((button) => {

    button.addEventListener("click", () => {

        const test = button.dataset.test;

        if (test === "allowed") {
            userIdInput.value = "user-1";
            roleInput.value = "user";
            methodInput.value = "GET";
            pathInput.value = "/api/profile";
            objectIdInput.value = "obj-1";
        }

        if (test === "bola") {
            userIdInput.value = "user-1";
            roleInput.value = "user";
            methodInput.value = "GET";
            pathInput.value = "/api/orders";
            objectIdInput.value = "obj-999";
        }

        if (test === "bfla") {
            userIdInput.value = "user-1";
            roleInput.value = "user";
            methodInput.value = "GET";
            pathInput.value = "/api/admin";
            objectIdInput.value = "";
        }

        form.requestSubmit();
    });

});


refreshEventsButton.addEventListener("click", loadEvents);


// Load existing events when dashboard opens
loadEvents();