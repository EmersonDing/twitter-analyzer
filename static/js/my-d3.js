/**
* Created by liuju on 11/21/2016.
*/
$("#keyword_network").on("click", function(){
    document.getElementById("streaming_tweets").style.backgroundColor = "lightslategrey";
    document.getElementById("keyword_network").style.backgroundColor = "darkblue";
    document.getElementById("streaming_tweets_div").style.display = "none";
    document.getElementById("keyword_network_div").style.display = "none";
    document.getElementById("keyword_search_div").style.display = "block";
});

function search_keyword(obj) {
    var search_keyword = $("#keyword_search_input").val();
    document.getElementById("keyword_network_div").style.display = "block";
    document.getElementById("keyword_search_div").style.display = "none";

    $.ajax({
        'url': get_canvas_data_url,
        'type': 'post',
        'data': {

        },
        'dataType': 'json',
        'success': function(data) {
            data.forEach(function(d) {
                d.Type = d["Type"];
                d.value = +d["Amount"];
            });

            //bubbles needs very specific format, convert data to this.
            var nodes = bubble.nodes({children:data}).filter(function(d) { return !d.children; });

            //setup the chart
            var bubbles = svg.append("g")
                .attr("transform", "translate(0,0)")
                .selectAll(".bubble")
                .data(nodes)
                .enter();

            //create the bubbles
            bubbles.append("circle")
                .attr("r", function(d){ return d.r; })
                .attr("cx", function(d){ return d.x; })
                .attr("cy", function(d){ return d.y; })
                .style("fill", function(d) { return color(d.value); })
                .on("click", function(d){
                    var keyword = d.Type;
                    console.log('The key word is : ' + keyword);
                    $.ajax({
                        'url': 'keyword_info',
                        'type': 'post',
                        'data': {
                            'keyword': keyword
                        },
                        'dataType': 'json',
                        'success': function(data) {
                            console.log(data);
                            document.getElementById("tweets").style.display = "block";
                            document.getElementById("chart").style.display = "none";
                        }
                    });
                });

            //format the text for each bubble
            bubbles.append("text")
                .attr("x", function(d){ return d.x; })
                .attr("y", function(d){ return d.y + 5; })
                .attr("text-anchor", "middle")
                .text(function(d){ return d["Type"]; })
                .style({
                    "fill":"white",
                    "font-family":"Helvetica Neue, Helvetica, Arial, san-serif",
                    "font-size": "12px"
                });
        }
    });
}

function return_to_search() {
    document.getElementById("keyword_network_div").style.display = "none";
    document.getElementById("keyword_search_div").style.display = "block";
}

function return_to_chart() {
    document.getElementById("tweets").style.display = "none";
    document.getElementById("chart").style.display = "block";
}

var diameter = 600, //max size of the bubbles
    color    = d3.scale.category20b(); //color category

var bubble = d3.layout.pack()
    .sort(null)
    .size([diameter, diameter])
    .padding(1.5);

var svg = d3.select("#d3_chart")
    .attr("align", "center")
    .append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .attr("class", "bubble");




// $.ajax({
//     'url': get_canvas_data_url,
//     'type': 'post',
//     'data': {
//
//     },
//     'dataType': 'json',
//     'success': function(data) {
//         data.forEach(function(d) {
//             d.Type = d["Type"];
//             d.value = +d["Amount"];
//         });
//
//         //bubbles needs very specific format, convert data to this.
//         var nodes = bubble.nodes({children:data}).filter(function(d) { return !d.children; });
//
//         //setup the chart
//         var bubbles = svg.append("g")
//             .attr("transform", "translate(0,0)")
//             .selectAll(".bubble")
//             .data(nodes)
//             .enter();
//
//         //create the bubbles
//         bubbles.append("circle")
//             .attr("r", function(d){ return d.r; })
//             .attr("cx", function(d){ return d.x; })
//             .attr("cy", function(d){ return d.y; })
//             .style("fill", function(d) { return color(d.value); })
//             .on("click", function(d){
//                 var keyword = d.Type;
//                 console.log('The key word is : ' + keyword);
//                 $.ajax({
//                     'url': 'keyword_info',
//                     'type': 'post',
//                     'data': {
//                         'keyword': keyword
//                     },
//                     'dataType': 'json',
//                     'success': function(data) {
//                         console.log(data);
//                         document.getElementById("tweets").style.display = "block";
//                         document.getElementById("chart").style.display = "none";
//                     }
//                 });
//             });
//
//         //format the text for each bubble
//         bubbles.append("text")
//             .attr("x", function(d){ return d.x; })
//             .attr("y", function(d){ return d.y + 5; })
//             .attr("text-anchor", "middle")
//             .text(function(d){ return d["Type"]; })
//             .style({
//                 "fill":"white",
//                 "font-family":"Helvetica Neue, Helvetica, Arial, san-serif",
//                 "font-size": "12px"
//             });
//     }
// });

// data.forEach(function(d) {
//     d.Type = d["Type"];
//     d.value = +d["Amount"];
// });
//
// //bubbles needs very specific format, convert data to this.
// var nodes = bubble.nodes({children:data}).filter(function(d) { return !d.children; });
//
// //setup the chart
// var bubbles = svg.append("g")
//     .attr("transform", "translate(0,0)")
//     .selectAll(".bubble")
//     .data(nodes)
//     .enter();
//
// //create the bubbles
// bubbles.append("circle")
//     .attr("r", function(d){ return d.r; })
//     .attr("cx", function(d){ return d.x; })
//     .attr("cy", function(d){ return d.y; })
//     .style("fill", function(d) { return color(d.value); })
//     .on("click", function(d){
//         var keyword = d.Type;
//         console.log('The key word is : ' + keyword);
//         $.ajax({
//             'url': 'keyword_info',
//             'type': 'post',
//             'data': {
//                 'keyword': keyword
//             },
//             'dataType': 'json',
//             'success': function(data) {
//                 console.log(data);
//                 document.getElementById("tweets").style.display = "block";
//                 document.getElementById("chart").style.display = "none";
//             }
//         });
//     });
//
// //format the text for each bubble
// bubbles.append("text")
//     .attr("x", function(d){ return d.x; })
//     .attr("y", function(d){ return d.y + 5; })
//     .attr("text-anchor", "middle")
//     .text(function(d){ return d["Type"]; })
//     .style({
//         "fill":"white",
//         "font-family":"Helvetica Neue, Helvetica, Arial, san-serif",
//         "font-size": "12px"
//     });