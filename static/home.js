var selectedRows = []

function arrowLogic(n) {
    table = document.getElementById("chargeTable");
    rows = table.rows;
    for (i = 0; i < rows.length; i++) {
        x = rows[0].getElementsByTagName("i")[i];
        console.log("I: " + i + " N: " + n);
        console.log(x.id);
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

function sortTable(n) {
    arrowLogic(n);
    identity = document.getElementById(n);
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("chargeTable")
    switching = true;
    dir = "asc";
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
            else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount ++;

        }
        else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

function checklist(n) {
    row = document.getElementById("row" + n);
    if (row.classList.contains("selected")) {
//        row.classList.remove("selected");
        var index = selectedRows.indexOf("row" + n);
        if (index > -1) {
            selectedRows.splice(index, 1);
        }
    }
    else {
//        row.classList.add("selected");
        selectedRows.push(row.id);
    }
    if (selectedRows.length > 0) {
        document.getElementById("deleteButton").style.display = "";
    }
    else {
        document.getElementById("deleteButton").style.display = "none";
    }
}

function toggle(source) {
    checkboxes = document.getElementsByName("row_check");
    for(i=0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}

function deleteFormSubmit() {
    var form = document.getElementById("deleteForm");
    form.submit();
}
