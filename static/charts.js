// Javascript file using Google Charting library to chart user data

var selected_chart = ""

// Parses in category info from JSON content and creates chart for it
function drawCategoryCaller(pie_category) {
    var parsed = JSON.parse(pie_category);
    google.charts.load('current', {'packages':['corechart']});
    drawCategory(parsed);
}

// Library call for drawing the category pie chart
function drawCategory(pie_category) {
    var pie_data = [['Category', 'Number of Purchases']];
     for (i = 0; i < pie_category.length; i++) {
        pie_data.push([pie_category[i]['Category'], pie_category[i]['Count']]);
     }
     google.charts.setOnLoadCallback(drawChart);
     function drawChart() {
        var data = google.visualization.arrayToDataTable(pie_data);
        var options = {
           backgroundColor: 'transparent',
           title: 'Categories',
        };
        var chart = new google.visualization.PieChart(document.getElementById('pie_category'));

        function selectHandler() {
            var selectedItem = chart.getSelection()[0];
            if (selectedItem) {
                var topping = data.getValue(selectedItem.row, 0);
                selected_chart = "category"
                formSubmit(topping, selected_chart);
            }
        }

        google.visualization.events.addListener(chart, 'select', selectHandler);
        chart.draw(data, options);
     }
}

// Parses in vendor info from JSON content and creates chart for it
function drawVendorCaller(pie_vendor) {
    var parsed = JSON.parse(pie_vendor);
    google.charts.load('current', {'packages':['corechart']});
    drawVendor(parsed);
}

// Library call for drawing the vendor pie chart
function drawVendor(pie_vendor) {
    var pie_data = [['Vendor', 'Number of Purchases']];
     for (i = 0; i < pie_vendor.length; i++) {
        pie_data.push([pie_vendor[i]['Vendor'], pie_vendor[i]['Count']]);
     }
     google.charts.setOnLoadCallback(drawChart);
     function drawChart() {
        var data = google.visualization.arrayToDataTable(pie_data);
        var options = {
           backgroundColor: 'transparent',
           title: 'Vendors',
        };
        var chart = new google.visualization.PieChart(document.getElementById('pie_vendor'));

        function selectHandler() {
            var selectedItem = chart.getSelection()[0];
            if (selectedItem) {
                var topping = data.getValue(selectedItem.row, 0);
                selected_chart = "vendor"
                formSubmit(topping, selected_chart);
            }
        }

        google.visualization.events.addListener(chart, 'select', selectHandler);
        chart.draw(data, options);
     }
}

// Parses in card info from JSON content and creates chart for it
function drawCardCaller(pie_card) {
    var parsed = JSON.parse(pie_card);
    google.charts.load('current', {'packages':['corechart']});
    drawCard(parsed);
}

// Library call for drawing the card pie chart
function drawCard(pie_card) {
    var pie_data = [['Card', 'Number of Purchases']];
     for (i = 0; i < pie_card.length; i++) {
        pie_data.push([pie_card[i]['Card'], pie_card[i]['Count']]);
     }
     google.charts.setOnLoadCallback(drawChart);
     function drawChart() {
        var data = google.visualization.arrayToDataTable(pie_data);
        var options = {
           backgroundColor: 'transparent',
           title: 'Cards',
        };
        var chart = new google.visualization.PieChart(document.getElementById('pie_card'));

        function selectHandler() {
            var selectedItem = chart.getSelection()[0];
            if (selectedItem) {
                var topping = data.getValue(selectedItem.row, 0);
                selected_chart = "card"
                formSubmit(topping, selected_chart);
            }
        }

        google.visualization.events.addListener(chart, 'select', selectHandler);
        chart.draw(data, options);
     }
}

// Submit option for piechart onclick
function formSubmit(topping, selected_chart) {
    if (selected_chart == 'category') {
        var input = document.getElementById("category_filter");
        input.value = topping;
    }

    if (selected_chart == 'vendor') {
        var input = document.getElementById("vendor_filter");
        input.value = topping;
    }

    if (selected_chart == 'card') {
        var input = document.getElementById("card_filter");
        input.value = topping;
    }

    var form = document.getElementById("pie_form");
    form.submit();
}
