/* ---------- Theme ---------- */
function toggleTheme() {
  const root = document.documentElement;
  const current = root.getAttribute("data-theme") || "light";
  const next = current === "dark" ? "light" : "dark";
  root.setAttribute("data-theme", next);
  localStorage.setItem("gs_theme", next);
  document.getElementById("theme-icon").textContent =
    next === "dark" ? "☀️" : "🌙";
  document.getElementById("theme-text").textContent =
    next === "dark" ? "Light Mode" : "Dark Mode";
}
(function initTheme() {
  const saved = localStorage.getItem("gs_theme") || "light";
  document.documentElement.setAttribute("data-theme", saved);
  const iconEl = document.getElementById("theme-icon");
  const textEl = document.getElementById("theme-text");
  if (saved === "dark") {
    if (iconEl) iconEl.textContent = "☀️";
    if (textEl) textEl.textContent = "Light Mode";
  }
})();

/* ---------- Loading spinner ---------- */
function showSpinner() {
  document.getElementById("loadingOverlay").style.display = "flex";
}

function hideSpinner() {
  document.getElementById("loadingOverlay").style.display = "none";
}

/* ---------- Generate Stars ---------- */
function generateStars(rating) {
  let r = parseFloat(rating);
  if (isNaN(r) || r <= 0) return "☆☆☆☆☆";
  const n = Math.round(r);
  return "★".repeat(n) + "☆".repeat(5 - n);
}

function renderStarSpans() {
  document.querySelectorAll(".rating-stars").forEach((el) => {
    el.textContent = generateStars(el.dataset.rating);
  });
}

/* ---------- Data extraction from DOM ---------- */
function getTableData() {
  const rows = [...document.querySelectorAll("#tableBody tr")];
  return rows.map((r) => {
    return {
      id: r.dataset.id,
      name: r.querySelector("td strong").textContent.trim(),
      rating: r.querySelector(".rating-value")
        ? r.querySelector(".rating-value").textContent.trim()
        : r.querySelector(".rating-stars").textContent.trim(),
      reviews: r.children[2].textContent.trim(),
      category: r.children[3].textContent.trim(),
      phone: r.children[4].textContent.trim(),
      status: r.dataset.status || r.children[5].innerText.trim(),
      address: r.dataset.address || "",
      distance:
        parseFloat(
          r.dataset.distance ||
            r.children[6].textContent.replace("km", "").trim()
        ) || 0,
      time: r.dataset.time || r.children[7].textContent.trim(),
      location_url: r.dataset.url || "#",
      rowEl: r,
    };
  });
}
let fullData = getTableData();
let viewData = [...fullData];
let currentPage = 1;
const itemsPerPage = 10; // show all by default; change if you want pagination
let sortColumn = null;
let sortDirection = "asc";

/* ---------- Render (reorders DOM rows) ---------- */
function renderRows(data) {
  const tbody = document.getElementById("tableBody");
  tbody.innerHTML = "";
  data.forEach((item) => {
    tbody.appendChild(item.rowEl);
  });
}

/* ---------- Sorting ---------- */
function sortTable(col) {
  if (sortColumn === col) {
    sortDirection = sortDirection === "asc" ? "desc" : "asc";
  } else {
    sortColumn = col;
    sortDirection = "asc";
  }
  viewData.sort((a, b) => {
    let av = a[col],
      bv = b[col];
    if (col === "distance" || col === "rating") {
      av = parseFloat(av) || 0;
      bv = parseFloat(bv) || 0;
    } else if (col === "reviews") {
      av = parseInt(av.replace(/[^0-9]/g, "")) || 0;
      bv = parseInt(bv.replace(/[^0-9]/g, "")) || 0;
    } else {
      av = (av || "").toString().toLowerCase();
      bv = (bv || "").toString().toLowerCase();
    }
    if (av < bv) return sortDirection === "asc" ? -1 : 1;
    if (av > bv) return sortDirection === "asc" ? 1 : -1;
    return 0;
  });
  updateSortHeaders();
  renderRows(viewData);
}
function updateSortHeaders() {
  document.querySelectorAll("th.sortable").forEach((th) => {
    th.classList.remove("sorted-asc", "sorted-desc");
    if (th.dataset.column === sortColumn) {
      th.classList.add(sortDirection === "asc" ? "sorted-asc" : "sorted-desc");
    }
  });
}

/* ---------- Filter ---------- */
function filterTable(term) {
  term = term.toLowerCase();
  viewData = fullData.filter((item) => {
    return Object.values(item).some((v) =>
      String(v).toLowerCase().includes(term)
    );
  });
  // after filter, re-sort with current sortColumn
  if (sortColumn) {
    sortTable(sortColumn);
  } else {
    renderRows(viewData);
  }
}

/* ---------- Row expansion ---------- */
function toggleRowExpansion(id) {
  console.log("Clicked row with ID:", id);
  const row = document.querySelector(`#tableBody tr[data-id="${id}"]`);
  if (!row) return;
  const existing = row.nextElementSibling;
  if (existing && existing.classList.contains("expanded-row")) {
    existing.remove();
    row.classList.remove("expanded");
    return;
  }

  // close others
  document
    .querySelectorAll("#tableBody tr.expanded")
    .forEach((r) => r.classList.remove("expanded"));
  document
    .querySelectorAll("#tableBody tr + .expanded-row")
    .forEach((er) => er.remove());
  row.classList.add("expanded");
  const item = viewData.find((d) => String(d.id) === String(id));
  const expanded = document.createElement("tr");
  expanded.className = "expanded-row";
  expanded.innerHTML = `<td colspan="10" class="expanded-content">
  <div class="expanded-item">
  <div class="expanded-label">Full Address</div>
  <div class="expanded-value">${item.address || "(no address)"}</div>
  </div>
  </td>`;
  row.parentNode.insertBefore(expanded, row.nextSibling);
}

/* ---------- Actions ---------- */
function openMaps(url) {
  window.open(url, "_blank");
}

/* ---------- CSV Export ---------- */
function exportToCSV() {
  const headers = [
    "Name",
    "Rating",
    "Reviews",
    "Category",
    "Phone",
    "Status",
    "Address",
    "Distance(km)",
    "Time",
    "MapURL",
  ];
  const lines = [headers.join(",")];
  viewData.forEach((it) => {
    const row = [
      `"${it.name.replace(/"/g, '""')}"`,
      it.rating,
      it.reviews,
      `"${it.category.replace(/"/g, '""')}"`,
      `"${it.phone.replace(/"/g, '""')}"`,
      `"${it.status.replace(/"/g, '""')}"`,
      `"${it.address.replace(/"/g, '""')}"`,
      it.distance,
      `"${it.time.replace(/"/g, '""')}"`,
      `"${it.location_url}"`,
    ];
    lines.push(row.join(","));
  });
  const blob = new Blob([lines.join("\n")], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "gscraper_results.csv";
  a.click();
  URL.revokeObjectURL(url);
  showToast("CSV exported!", "success");
}

/* ---------- Toast ---------- */
function showToast(msg, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.classList.add("show"), 100);
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

/* ---------- Init after DOM load ---------- */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("searchForm");
  if (form) {
    form.addEventListener("submit", () => {
      showSpinner();
    });
  }
  // Render star
  renderStarSpans();
  // Collect fresh data from DOM (after Django rendered rows)
  fullData = getTableData();
  viewData = [...fullData];
  // Row click expand
  document.querySelectorAll("#tableBody tr").forEach((tr) => {
    tr.addEventListener("click", () => toggleRowExpansion(tr.dataset.id));
  });
  // Sort header clicks
  document.querySelectorAll("th.sortable").forEach((th) => {
    th.addEventListener("click", () => sortTable(th.dataset.column));
  });
  // Filter input
  document
    .getElementById("filterInput")
    .addEventListener("input", (e) => filterTable(e.target.value));
});
