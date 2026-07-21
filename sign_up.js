const signup = document.getElementById("button");
const name = document.getElementById("name");
const pw = document.getElementById("password");

signup.addEventListener("click", function(event) {
    event.preventDefault();
    fetch("http://127.0.0.1:8000/daftar", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: name.value, password: pw.value})
    })
    .then(response => response.json())
    .then(data => document.getElementById("info").textContent = data.pesan);

});