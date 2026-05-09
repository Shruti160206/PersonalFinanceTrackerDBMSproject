// Subscriptions page effects
const subscriptionRows = document.querySelectorAll("tbody tr");

subscriptionRows.forEach((row) => {
  row.addEventListener("mouseover", () => {
    row.style.backgroundColor = "#f5f5f5";
    row.style.transition = "0.3s";
  });

  row.addEventListener("mouseout", () => {
    row.style.backgroundColor = "";
  });
});

// Highlight inactive subscriptions
const inactiveSubs = document.querySelectorAll(".status.inactive");

inactiveSubs.forEach((status) => {
  status.style.opacity = "0.7";
});