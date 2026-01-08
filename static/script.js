async function loadData() {
  const token = localStorage.getItem("token");
  const res = await fetch("/companies/", {
    headers: { "Authorization": "Bearer " + token }
  });

  const data = await res.json();
  $("#tbl").DataTable({
    data,
    destroy: true,
    columns: [
      { data: "id" },
      { data: "index" },
      { data: "name_fa" },
      { data: "name_en" },
      { data: "website" },
      { data: "file_number" },
      { data: "sector" },
      { data: "country" }
    ],
    initComplete: function () {
      let api = this.api();

      api.columns().every(function (index) {
        let column = this;
        $("thead tr.filters th:eq(" + index + ") input").on("keyup change", function () {
          column.search(this.value).draw();
        });
      });
    }
  });
}


loadData();


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

  loadData(); // reload table correctly
}
