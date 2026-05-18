// Optional: mark unread notifications visually
const unreadStatus = document.querySelectorAll(".status.active");

unreadStatus.forEach((status) => {
  status.style.color = "green";
  status.style.fontWeight = "bold";
});