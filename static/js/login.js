const form = document.getElementById("loginForm");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = {
        email: document.querySelector("[name='email']").value,
        password: document.querySelector("[name='password']").value
    };

    const response = await fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    });

    const data = await response.json();

    const msgBox = document.getElementById("message-box");

    if (response.ok) {
        msgBox.innerHTML = `
            <div class="flash-message flash-success">
                ${data.message || "Login successful"}
            </div>
        `;

        setTimeout(() => {
            window.location.href = "/dashboard";
        }, 800);

    } else {
        msgBox.innerHTML = `
            <div class="flash-message flash-error">
                ${data.error || "Invalid credentials"}
            </div>
        `;
    }
});