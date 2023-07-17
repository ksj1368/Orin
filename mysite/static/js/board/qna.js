document.querySelectorAll("#qnatable tr").forEach(el => {
    el.addEventListener("mouseenter", (e) => {
      e.currentTarget.classList.add("table-active");
    });
    el.addEventListener("mouseleave", (e) => {
      e.currentTarget.classList.remove("table-active");
    });
  });
  
  