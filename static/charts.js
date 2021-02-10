function draw(pie_count) {
    var parsed = JSON.parse(pie_count);
    google.charts.load('current', {'packages':['corechart']});
    pieChart(parsed);
}

function pieChart(pie_count) {
    var pieData = [['Category', 'Number of Purchases']];
     for (i = 0; i < pie_count.length; i++) {
        pieData.push([pie_count[i]['Category'], pie_count[i]['Count']]);
     }
     google.charts.setOnLoadCallback(drawChart);
     function drawChart() {
        var data = google.visualization.arrayToDataTable(pieData);
        var options = {
           backgroundColor: 'transparent',
           title: 'Charges',
           animation:{
                duration: 1000,
                easing: 'out',
                startup: true,
           }
        };
        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

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

    var form = document.getElementById("pieForm");
    form.submit();
}
