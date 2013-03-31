/*global window, console, d3 */

(function(exports, $){
  "use strict";

  var data;

  var elbiToUrl = function(elbi){
    return $('#elbi-' + elbi + ' > a').prop('href');
  };

  // dump data into bins according to keyAccessor
  // is this the same as d3.layout .hierarchy?
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
    var bins = binData(data, function(d){
      var key = d.name_1[0];
      if ($.isNumeric(key)){
        return "0";
      }
      return key.toUpperCase();
    });
    var binArray = [];
    $.each(bins, function(k, v){
      binArray.push({
        name: k,
        buildings: v
      });
    });
    binArray = binArray.sort(function(a, b) { return b.name < a.name ? 1 : -1; });
    prepBinsHtml(binArray);
  };

  var prepBinsHtml = function(bins){
    var binContainer = d3.select('#name');
    console.log(binContainer, bins);
    binContainer.selectAll('.bin').data(bins)
      .enter()
        .append('div')
        .attr('class', 'bin')
        .html(function(d){ return d.name; });
  };

  var init = function(data){
    window.data = data; // DEBUG
    prepNameData(data);
  };

  $.getJSON('/chart/search/data/', init);

})(window, window.jQuery);
