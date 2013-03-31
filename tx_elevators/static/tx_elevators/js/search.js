/*global window, console */

(function(exports, $){
  "use strict";

  var data;

  var elbiToUrl = function(elbi){
    return $('#elbi-' + elbi + ' > a').prop('href');
  };

  // dump data into bins according to keyAccessor
  var binData = function(data, keyAccessor){
    var bin = {},
        d;
    for (var i = 0; i < data.length; i++){
      d = data[i];
      if (!bin[keyAccessor(d)]) {
        bin[keyAccessor(d)] = [];
      }
      bin[keyAccessor(d)].push(d);
    }
    return bin;
  };

  var prepNameData = function(data){
    var bin = binData(data, function(d){
      var key = d.name_1[0];
      if ($.isNumeric(key)){
        return "0";
      }
      return key.toUpperCase();
    });
    console.log(bin);
  };

  var init = function(data){
    window.data = data; // DEBUG
    prepNameData(data);
  };

  $.getJSON('/chart/search/data/', init);

})(window, window.jQuery);
