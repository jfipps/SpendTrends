function arrowLogic(n) {
    table = document.getElementById("chargeTable");
    rows = table.rows;
    for (i = 0; i < (rows.length - 1); i++) {
        x = rows[0].getElementsByTagName("i")[i];
        if (i != n) {
            x.style.display = "none";
        }
        else {
            if (x.classList.contains("up")) {
                x.classList.remove("up");
                x.classList.add("down");
            }
            else {
                x.classList.remove("down");
                x.classList.add("up");
            }
            x.style.display = "";
        }
    }
}

function sortTable(table, columnIndex, asc = true) {
//    arrowLogic();
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll('tr'));
    //Sort Rows
    //Sorts any column not involving money
    if (columnIndex != 3) {
        var sortedRows = rows.sort((a, b) => {
            var aColText = a.querySelector(`td:nth-child(${ columnIndex + 1})`).textContent.trim();
            var bColText = b.querySelector(`td:nth-child(${ columnIndex + 1})`).textContent.trim();
            return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
        });
    }
    //Sorts column based on money
    //Turns to float to compare
    else {
        var sortedRows = rows.sort((a, b) => {
            var aColText = a.querySelector(`td:nth-child(${ columnIndex + 1})`).textContent.trim();
            var bColText = b.querySelector(`td:nth-child(${ columnIndex + 1})`).textContent.trim();
            aColFloat = Number(aColText.replace(/(^\$|,)/g,''));
            bColFloat = Number(bColText.replace(/(^\$|,)/g,''));
            return aColFloat > bColFloat ? (1 * dirModifier) : (-1 * dirModifier);
        });
    }
    //Remove all TRs from table
    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }

    //Re-add sorted rows
    tBody.append(...sortedRows);

    // Remember how column is sorted
    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
    table.querySelector(`th:nth-child(${ columnIndex + 1})`).classList.toggle("th-sort-asc", asc);
    table.querySelector(`th:nth-child(${ columnIndex + 1})`).classList.toggle("th-sort-desc", !asc);
}

//Initiates functions for table head onclick
window.onload = function() {
    document.querySelectorAll(".table-sortable th").forEach(headerCell => {
        headerCell.addEventListener("click", () => {
            const tableElement = headerCell.parentElement.parentElement.parentElement;
            const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
            const currentIsAscending = headerCell.classList.contains("th-sort-asc");

            sortTable(tableElement, headerIndex, !currentIsAscending);
       });
    });
}

//Checks all checkboxes
function checklist(n) {
    row = document.getElementById("row" + n);
    if (row.classList.contains("selected")) {
        var index = selectedRows.indexOf("row" + n);
        if (index > -1) {
            selectedRows.splice(index, 1);
        }
    }
    else {
        selectedRows.push(row.id);
    }
    if (selectedRows.length > 0) {
        document.getElementById("deleteButton").style.display = "";
    }
    else {
        document.getElementById("deleteButton").style.display = "none";
    }
}

//Toggles individual checkboxes
function toggle(source) {
    checkboxes = document.getElementsByName("row_check");
    for(i=0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}

//Submit function for delete modal
function deleteFormSubmit() {
    var form = document.getElementById("deleteForm");
    form.submit();
}
