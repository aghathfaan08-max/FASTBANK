const hero = document.getElementById("sapa");

const saldo = document.getElementById("saldo");

const token = localStorage.getItem("token");

fetch("http://127.0.0.1:8000/home", {
    method: "GET",
    headers: {"Authorization": "Bearer " + token}

})
.then(response => response.json())
.then(data => 
{hero.textContent = "halo " + data.nama; 
    saldo.textContent = "saldo anda " + data.saldo + " rupiah";
}
);