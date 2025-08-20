document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const chatBox = document.getElementById("chat-box");

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    // Display user's message
    chatBox.innerHTML += `<div><strong>You:</strong> ${message}</div>`;

    // Call Flask API
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    chatBox.innerHTML += `<div><strong>Bot:</strong> ${data.reply}</div>`;

    chatInput.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
  });
});
