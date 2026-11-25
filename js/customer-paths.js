document.querySelectorAll("[data-customer-path]").forEach((link) => {
  link.addEventListener("click", () => {
    if (typeof window.gtag !== "function") return;
    window.gtag("event", "customer_path_click", {
      customer_path: link.dataset.customerPath,
      page_path: window.location.pathname,
    });
  });
});

const printChecklist = document.getElementById("print-well-checklist");
if (printChecklist) {
  printChecklist.hidden = false;
  printChecklist.addEventListener("click", () => {
    if (typeof window.gtag === "function") {
      window.gtag("event", "well_checklist_print");
    }
    window.print();
  });
}
