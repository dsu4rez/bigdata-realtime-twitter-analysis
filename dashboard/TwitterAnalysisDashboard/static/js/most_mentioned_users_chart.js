var ctx = document.getElementById('most_mentioned_users_chart').getContext('2d');

var most_mentioned_users_chart = new Chart(ctx, {
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

var src_data_most_mentioned_users = {
    labels: [],
    negative: [],
    neutral: [],
    positive: []
}

setInterval(function(){
    $.getJSON('/refresh_most_mentioned_users', {
    }, function(data) {
        src_data_most_mentioned_users.labels = data.sLabel;
        src_data_most_mentioned_users.negative = data.sNegative;
        src_data_most_mentioned_users.neutral = data.sNeutral;
        src_data_most_mentioned_users.positive = data.sPositive;
    });
    most_mentioned_users_chart.data.labels = src_data_most_mentioned_users.labels;
    most_mentioned_users_chart.data.datasets[0].data = src_data_most_mentioned_users.negative;
    most_mentioned_users_chart.data.datasets[1].data = src_data_most_mentioned_users.neutral;
    most_mentioned_users_chart.data.datasets[2].data = src_data_most_mentioned_users.positive;
    most_mentioned_users_chart.update();
},2000);