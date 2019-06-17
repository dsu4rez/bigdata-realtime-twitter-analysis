var ctx = document.getElementById('most_active_users_chart').getContext('2d');

var most_active_users_chart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
        labels: [],

        datasets: [{
            label: "Negative",
            data: [],
            backgroundColor: "rgba(194, 67, 67, 0.6)"
        },{
            label: "Neutral",
            data: [],
            backgroundColor: "rgba(170, 184, 194, 0.6)"
        },{
            label: "Positive",
            data: [],
            backgroundColor: "rgba(67, 194, 122, 0.6)"
        }]
    },
    options: {
        scales: {
            xAxes: [{
                stacked: true,
                ticks: {
                    beginAtZero: true,
                    callback: function(value) {if (value % 1 === 0) {return value;}}
                }
            }],
            yAxes: [{
                stacked: true
            }]
        }
    }
});

src_data_most_active_users_labels = [];
src_data_most_active_users_negative = [];
src_data_most_active_users_neutral = [];
src_data_most_active_users_positive = [];

setInterval(function(){
    $.getJSON('/refresh_most_active_users', {
    }, function(data) {
        src_data_most_active_users_labels = data.sLabel;
        src_data_most_active_users_negative = data.sNegative;
        src_data_most_active_users_neutral = data.sNeutral;
        src_data_most_active_users_positive = data.sPositive;
    });
    most_active_users_chart.data.labels = src_data_most_active_users_labels;
    most_active_users_chart.data.datasets[0].data = src_data_most_active_users_negative;
    most_active_users_chart.data.datasets[1].data = src_data_most_active_users_neutral;
    most_active_users_chart.data.datasets[2].data = src_data_most_active_users_positive;
    most_active_users_chart.update();
},2000);
