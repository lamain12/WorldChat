let username = "";
let socket = null;
const url = "http://127.0.0.1:8000";

function signup() {
  username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  fetch(url+"/signup", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username, password})
  }).then(res => res.json()).then(data => alert(data.message));
}

function login() {
  username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  fetch(url+"/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username, password})
  }).then(res => {
    if (res.ok) {
      document.getElementById("auth-section").style.display = "none";
      document.getElementById("chat-section").style.display = "block";
      document.getElementById("logged-in-user").textContent = username;
      startSocket();
    }
  });
}

function startSocket() {
  socket = new WebSocket(`ws://localhost:8000/ws/${username}`);
  socket.onmessage = (event) => {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div>${event.data}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
  };
}

function sendMessage() {
  const recipient = document.getElementById("recipient").value;
  const message = document.getElementById("message").value;
  const formatted = recipient ? `to:${recipient} ${message}` : message;
  socket.send(formatted);
}
