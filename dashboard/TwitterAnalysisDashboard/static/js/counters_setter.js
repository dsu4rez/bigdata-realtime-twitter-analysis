var total_text = document.getElementById('total_counter_value');
var speed_text = document.getElementById('analysis_speed_value');
var negative_text = document.getElementById('negative_counter');
var neutral_text = document.getElementById('neutral_counter');
var positive_text = document.getElementById('positive_counter');

var src_Total = 0;
var src_Positive = 0;
var src_Neutral = 0;
var src_Negative = 0;

setInterval(function(){
    $.getJSON('/refresh_tweet_counters', {
    }, function(data) {
        src_Total = parseInt(data.sTotal);
        src_Negative = parseInt(data.sNegative);
        src_Neutral = parseInt(data.sNeutral);
        src_Positive = parseInt(data.sPositive);
    });

    negative_text.textContent = src_Total > 0 ? Math.trunc(src_Negative/src_Total*100) + "%" : 0 + "%";
    neutral_text.textContent = src_Total > 0 ? Math.trunc(src_Neutral/src_Total*100) + "%" : 0 + "%";
    positive_text.textContent = src_Total > 0 ? Math.trunc(src_Positive/src_Total*100) + "%" : 0 + "%";

    total_text.textContent = src_Total;
    //speed_text.textContent = Math.trunc(src_Total/30) + " tweets/min"

},2000);