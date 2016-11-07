/**
* Created by liuju on 11/6/2016.
*/
function create_chart_device(data) {
    console.log('create_chart_device');
    var chart = AmCharts.makeChart( "chart", {
      "type": "serial",
      "theme": "light",
      "dataProvider": data,
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
}


function create_chart_lang(data) {
    var chart = AmCharts.makeChart( "chart", {
        "type": "pie",
        "theme": "light",
        "dataProvider": data,
        "valueField": "tweets",
        "titleField": "Type",
        "balloon":{
        "fixedPosition":true
        },
        "export": {
        "enabled": false
        }
    } );
}
