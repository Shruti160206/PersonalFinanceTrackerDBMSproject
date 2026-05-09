// Notifications page effects
const notificationRows = document.querySelectorAll("tbody tr");

notificationRows.forEach((row) => {
  row.addEventListener("mouseover", () => {
    row.style.backgroundColor = "#f5f5f5";
    row.style.transition = "0.3s";
  });

  row.addEventListener("mouseout", () => {
    row.style.backgroundColor = "";
  });
});

// Optional: mark unread notifications visually
const unreadStatus = document.querySelectorAll(".status.active");

unreadStatus.forEach((status) => {
  status.style.fontWeight = "bold";
});