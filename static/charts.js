// Javascript file using Google Charting library to chart user data

// Parses in user info from JSON content and creates chart for it
function draw(pie_category) {
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
                formSubmit(topping);
            }
        }

        google.visualization.events.addListener(chart, 'select', selectHandler);
        chart.draw(data, options);
     }
}

function formSubmit(topping) {
    var input = document.getElementById("category_filter");
    input.value = topping;

    console.log(input);

    var form = document.getElementById("pie_form");
    form.submit();
}
