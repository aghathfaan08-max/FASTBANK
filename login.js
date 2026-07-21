
const name = document.getElementById("name");

const password = document.getElementById("password");

const submit = document.getElementById("button");

submit.addEventListener("click", function(event) {
    event.preventDefault();
    fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: name.value, password: password.value})
    })
    .then(response => response.json())
    .then(data => {document.getElementById("info").textContent = data.pesan;
if (data.acces_token) {
    localStorage.setItem("token", data.acces_token);
    window.location.href = "home.html";
}
});
});
