// loans page effects
const loanRows = document.querySelectorAll("tbody tr");

loanRows.forEach((row) => {
  row.addEventListener("mouseover", () => {
    row.style.backgroundColor = "#f5f5f5";
    row.style.transition = "0.3s";
  });

  row.addEventListener("mouseout", () => {
    row.style.backgroundColor = "";
  });
});