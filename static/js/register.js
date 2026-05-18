document.getElementById("registerForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    console.log("clicked submit button");

    const formData = {
        first_name: document.querySelector("[name='first_name']").value,
        last_name: document.querySelector("[name='last_name']").value,
        email: document.querySelector("[name='email']").value,
        date_of_birth: document.querySelector("[name='date_of_birth']").value,
        password: document.querySelector("[name='password']").value,
        confirm_password: document.querySelector("[name='confirm_password']").value
    };

    console.log(formData)

    const response = await fetch("/api/register", {
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
                ${data.message || "User created successfully"}
            </div>
        `;
        setTimeout(() => {
            window.location.href = "/login";
        }, 800);

    } else {
        msgBox.innerHTML = `
            <div class="flash-message flash-error">
                ${data.error || "Something went wrong"}
            </div>
        `;
    }
});