/*global window, console, d3 */

(function(exports, $){
  "use strict";

  var _data;

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

  var nameComparator = function(a, b){
    return b.name < a.name ? 1 : -1;
  };

  var prepNameData = function(data){
    _data = data;
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
    binArray = binArray.sort(nameComparator);
    prepBinsHtml(binArray);
  };

  var prepBinsHtml = function(binArray){
    var binContainer = d3.select('#name');
    $('#name input').on('keypress', function(){
      var needle = this.value.toUpperCase();
      var filtered = _data.filter(function(d){ return d.name_1.indexOf(needle) !== -1; });
      console.log(filtered.length);
    });
    var bins = binContainer.selectAll('.bin').data(binArray)
      .enter()
        .append('div')
        .attr('class', 'bin span3')
        .html(function(d){ return '<h4>' + d.name + '</h4>'; });
    var lists = bins.selectAll('.list').data(function(d) { return [d]; })
      .enter()
        .append('div')
        .attr('class', 'list');
    lists.selectAll('.item').data(function(d){ return d.buildings; })
      .enter()
        .append('div')
        .attr('class', 'item')
        .text(function(d){ return d.name_1; })
        .style('display', 'none');
  };

  var init = function(data){
    window.data = data; // DEBUG
    prepNameData(data);
  };

  $.getJSON('/chart/search/data/', init);

})(window, window.jQuery);
