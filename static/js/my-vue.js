/**
 * Created by liuju on 11/23/2016.
 */
// This is the js for the twitter_analyzer/index.html view.

var app = function(data) {

    var self = {};

    Vue.config.silent = false; // show all warnings

    self.get_tweets_list = function() {
        $.post(get_tweets_info_url,
            {

            },
            function(data) {
                self.vue.tweets_list = data;
                console.log(self.vue.tweets_list);
            }
        );
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            tweets_list: []
        },
        methods: {
            get_tweets_list: self.get_tweets_list
        }

    });

    // pass the data into app when initiated.
    self.vue.tweets_list = data;
    $("#vue-div").show();



    return self;
};

var APP = null;
