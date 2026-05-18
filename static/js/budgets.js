// Animate progress bars on load
window.addEventListener('load', () => {
  document.querySelectorAll('.progress-bar[data-pct]').forEach(bar => {
    bar.style.width = '0';
    requestAnimationFrame(() => {
      setTimeout(() => {
        bar.style.width = Math.min(parseFloat(bar.dataset.pct), 100) + '%';
      }, 80);
    });
  });
});

// Auto-submit month/year form on change
document.querySelectorAll('.month-select select').forEach(sel => {
  sel.addEventListener('change', () => sel.closest('form').submit());
});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("budgetForm");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const messageBox = document.getElementById("budgetMessageBox");
    messageBox.style.marginBottom = "10px";

    const formData = {
      category_id: document.querySelector("[name='category_id']").value,
      limit_amount: document.querySelector("[name='limit_amount']").value,
      month: document.querySelector("[name='month']").value,
      year: document.querySelector("[name='year']").value
    };

    try {
      const response = await fetch("/api/budgets", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        messageBox.textContent = data.message || "Budget created successfully";
        messageBox.style.color = "green";

        form.reset();

        setTimeout(() => {
          closeModal("addBudgetModal");
          window.location.reload();
        }, 600);

      } else {
        messageBox.textContent = data.error || "Failed to create budget";
        messageBox.style.color = "red";
      }

    } catch (err) {
      messageBox.textContent = "Server error. Please try again.";
      messageBox.style.color = "red";
    }
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const deleteButtons = document.querySelectorAll(".delete-budget-btn");
  deleteButtons.forEach(button => {
    button.addEventListener("click", async () => {
      const budgetId = button.dataset.budgetId;
      const confirmed = confirm( "Are you sure you want to delete this budget?");
      if (!confirmed) return;

      try {
        const response = await fetch(`/api/budgets/${budgetId}`, {
          method: "DELETE"
        });
        const data = await response.json();

        if (response.ok) {
          const row = document.getElementById(`budget-row-${budgetId}`);
          if (row) {
            row.remove();
          }
        } else {
          alert(data.error || "Failed to delete budget");
        }
      } catch (err) {
        alert("Server error. Please try again.");
      }
    });
  });
});