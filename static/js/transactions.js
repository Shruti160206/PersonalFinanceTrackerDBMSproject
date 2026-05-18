// set today's date as default in add form
const dateInput = document.getElementById('tx_date');
if (dateInput) dateInput.valueAsDate = new Date();

// create transaction
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("transactionForm");
  const messageBox = document.getElementById("txMessageBox");

  function showMessage(type, text) {
    messageBox.className = `form-message ${type}`;
    messageBox.textContent = text;
  }

  function clearMessage() {
    messageBox.className = "form-message";
    messageBox.textContent = "";
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    clearMessage();

    const formData = {
      amount: document.querySelector("[name='amount']").value,
      category_id: document.querySelector("[name='category_id']").value,
      transaction_date: document.querySelector("[name='transaction_date']").value
    };

    console.log(formData);

    try {
      const response = await fetch("/api/transactions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        showMessage("success", data.message || "Transaction created successfully");

        form.reset();

        setTimeout(() => {
          window.location.reload();
        }, 800);

      } else {
        showMessage("error", data.error || "Failed to create transaction");
      }

    } catch (err) {
      showMessage("error", "Server error. Please try again.");
    }
  });
});

// delete transaction
document.addEventListener("DOMContentLoaded", () => {
  const deleteButtons = document.querySelectorAll(".delete-transaction-btn");

  deleteButtons.forEach(button => {
    button.addEventListener("click", async () => {
      const transactionId = button.dataset.transactionId;
      const confirmed = confirm(
        "Are you sure you want to delete this transaction?"
      );
      if (!confirmed) return;

      try {
        const response = await fetch(
          `/api/transactions/${transactionId}`,
          { method: "DELETE" }
        );

        const data = await response.json();
        if (response.ok) {
          button.closest("tr").remove();
        } else {
          alert(data.error || "Failed to delete transaction");
        }

      } catch (err) {
        alert("Server error. Please try again.");
      }
    });
  });
});
