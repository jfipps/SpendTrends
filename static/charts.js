function piegraph() {
    var pieData = [
                {% for pie_slice, colors in set %}
                    {
                        value: {{pie_slice['Count']}},
                        label: "{{pie_slice['Category']}}",
                        color: "{{colors}}"
                    },
                {% endfor %}
            ];

            //get bar chart canvas
            var mychart = document.getElementById("chart").getContext("2d");
            steps = 10;
            max = {{ max }}
            //draw pie chart
            new Chart(document.getElementById("chart").getContext("2d")).Pie(pieData);
}