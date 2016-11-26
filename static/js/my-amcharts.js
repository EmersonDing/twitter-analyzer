/**
* Created by liuju on 11/21/2016.
*/

// Go to Streaming Tweets function.
$("#streaming_tweets").on("click",function(){
    document.getElementById("streaming_tweets").style.backgroundColor = "darkblue";
    document.getElementById("keyword_network").style.backgroundColor = "lightslategrey";
    document.getElementById("streaming_tweets_div").style.display = "block";
    document.getElementById("keyword_graph").style.display = "none";
});

var chart = null;
var is_completed = false;
var timer_id = 0;

function cancel_chart() {
    console.log('cancel-chart');
    // cancel the tweepy streamlistener.
    $.post(cancel_chart_data_url);
}

function get_chart() {
    document.getElementById("btn_waiting").style.display = "block";
    document.getElementById("btn_completed").style.display = "none";

    var search_text = $("#search").val();
    var type_of_analysis = $("#type_of_analysis").val();
    var number_of_item = $("#number_of_item").val();
    var number_of_tweet = $("#number_of_tweet").val();
    is_completed = false;

    // Chart
    chart = AmCharts.makeChart( "chart", {
      "type": "serial",
      "theme": "light",
      "dataProvider": {},
      "valueAxes": [ {
        "gridColor": "#FFFFFF",
        "gridAlpha": 0.2,
        "dashLength": 0
      } ],
      "gridAboveGraphs": true,
      "startDuration": 1,
      "graphs": [ {
        "balloonText": "[[category]]: <b>[[value]]</b>",
        "fillAlphas": 0.8,
        "lineAlpha": 0.2,
        "type": "column",
        "valueField": "tweets"
      } ],
      "chartCursor": {
        "categoryBalloonEnabled": false,
        "cursorAlpha": 0,
        "zoomable": false
      },
      "categoryField": "Type",
      "categoryAxis": {
        "gridPosition": "start",
        "gridAlpha": 0,
        "tickPosition": "start",
        "tickLength": 20
      },
      "export": {
        "enabled": false
      }

    } );

    // streaming the tweets data.
    $.ajax({
        'url': get_chart_data_url,
        'type': 'post',
        'data': {
            'search_text': search_text,
            'type_of_analysis': type_of_analysis,
            'number_of_item': number_of_item,
            'number_of_tweet': number_of_tweet
        },
        'dataType': 'json',
        'success': function(data) {
            chart.dataProvider = data;
            chart.validateData();
            is_completed = true;
            // stop the continuous ajax call when the entire data is received.
            clearInterval(timer_id);
            document.getElementById("btn_waiting").style.display = "none";
            document.getElementById("btn_completed").style.display = "block";
        }
    });

    // initiate the continuous ajax call to update the chart in every two seconds,
    // so the chart will be lively updated.
    timer_id = setInterval(function() {
        if (!is_completed) {
            // Ajax call to get chart data from server.
            $.ajax({
                'url': get_realtime_update_url,
                'type': 'post',
                'data': {
                    'search_text': search_text,
                    'type_of_analysis': type_of_analysis,
                    'number_of_item': number_of_item
                },
                'dataType': 'json',
                'success': function (data) {
                    chart.dataProvider = data;
                    chart.validateData();
                }
            });
        }
    }, 2000); // the default interval is 2000 ms.
}