// script.js
// Purpose: Handles chat widget behavior — sending messages to the backend
// and displaying responses.

// Change this to your Render URL once deployed, e.g.:
// const API_URL = "https://your-app.onrender.com/chat";
const API_URL = "/chat";

const messagesEl = document.getElementById("chat-messages");
const inputEl = document.getElementById("chat-input");
const sendBtn = document.getElementById("chat-send");

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = "msg " + (sender === "user" ? "user-msg" : "bot-msg");
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;

  addMessage(text, "user");
  inputEl.value = "";

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    const data = await res.json();
    addMessage(data.response, "bot");
  } catch (err) {
    addMessage("Sorry, something went wrong. Please try again.", "bot");
    console.error(err);
  }
}

sendBtn.addEventListener("click", sendMessage);
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});