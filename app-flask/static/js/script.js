async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    if (!file) return alert("Please select a file to upload.");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        const result = await response.json();
        addFileToList(result.filename);
        checkStatus();
    } else {
        alert("File upload failed.");
    }
}

function addFileToList(filename) {
    const fileList = document.getElementById("fileList");
    const li = document.createElement("li");
    li.innerHTML = `${filename} <span class="status-icon" id="status-${filename}">⏳</span>`;
    fileList.appendChild(li);
}

async function checkStatus() {
    const response = await fetch("/status");
    const statuses = await response.json();

    for (const [filename, info] of Object.entries(statuses)) {
        const statusIcon = document.getElementById(`status-${filename}`);
        if (statusIcon) {
            statusIcon.textContent = info.status === "success" ? "✅" : "❌";
            statusIcon.style.color = info.status === "success" ? "green" : "red";
        }
    }
}

async function sendMessage() {
    const userInput = document.getElementById("userInput");
    const message = userInput.value;
    if (!message) return;

    const chatBox = document.getElementById("messages");
    chatBox.innerHTML += `<div><b>You:</b> ${message}</div>`;

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const result = await response.json();
    chatBox.innerHTML += `<div><b>Bot:</b> ${result.response}</div>`;
    userInput.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
}