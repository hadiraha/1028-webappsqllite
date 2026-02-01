async function loadData() {
  const token = localStorage.getItem("token");

  const res = await fetch("/companies/", {
    headers: { "Authorization": "Bearer " + token }
  });

  const data = await res.json();

  // Column indexes containing Farsi content
  const FARSI_COLUMNS = [2, 5, 6, 8, 9];

  $("#tbl").DataTable({
    data: data,
    destroy: true,

    columns: [
      { data: "id" },
      { data: "index" },
      { data: "name_fa" },
      { data: "name_en" },
      { data: "website" },
      { data: "website_desc" },
      { data: "magazine_desc" },
      { data: "file_number" },
      { data: "sector" },
      { data: "country" }
    ],

    columnDefs: [
      {
        targets: FARSI_COLUMNS,
        createdCell: function (td) {
          td.classList.add("rtl");
        }
      }
    ],

    initComplete: function () {
      const api = this.api();

      api.columns().every(function (index) {
        const column = this;
        const input = $("thead tr.filters th:eq(" + index + ") input");

        if (!input.length) return;

        // Apply RTL to Farsi filter inputs
        if (FARSI_COLUMNS.includes(index)) {
          input.addClass("rtl");
        }

        // Prevent sorting when clicking inside filter input
        input.on("click", function (e) {
          e.stopPropagation();
        });

        // Column search
        input.on("keyup change", function () {
          column.search(this.value).draw();
        });
      });
    }
  });
}

// Initial load
loadData();

// =====================
// Auth & Actions
// =====================

function logout() {
  localStorage.removeItem("token");
  window.location = "/static/login.html";
}

async function uploadExcel() {
  const fileInput = document.getElementById("file");

  if (!fileInput.files.length) {
    alert("Please select file");
    return;
  }

  const form = new FormData();
  form.append("file", fileInput.files[0]);

  const token = localStorage.getItem("token");

  const res = await fetch("/companies/upload", {
    method: "POST",
    headers: {
      "Authorization": "Bearer " + token
    },
    body: form
  });

  if (!res.ok) {
    alert("Upload failed (auth or server error)");
    return;
  }

  const data = await res.json();
  alert("Imported: " + data.imported_rows + " rows");

  loadData();
}

async function deleteAll() {
  if (!confirm("⚠️ Are you sure?\nThis will DELETE ALL data permanently.")) {
    return;
  }

  const token = localStorage.getItem("token");

  const res = await fetch("/companies/delete-all", {
    method: "DELETE",
    headers: {
      "Authorization": "Bearer " + token
    }
  });

  if (!res.ok) {
    alert("Delete failed (auth or server error)");
    return;
  }

  alert("All data deleted");
  loadData();
}