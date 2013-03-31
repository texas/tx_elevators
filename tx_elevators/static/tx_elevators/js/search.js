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
  var buildingNameComparator = function(a, b){
    return b.name_1 < a.name_1 ? 1 : -1;
  };

  var prepNameData = function(data){
    var bins = binData(data, function(d){
      var key = d.name_1[0];
      if ($.isNumeric(key)){
        return "0&ndash;9";
      }
      return key.toUpperCase();
    });

    var binArray = [];
    $.each(bins, function(k, v){
      binArray.push({
        name: k,
        buildings: v.sort(buildingNameComparator)
      });
    });
    binArray = binArray.sort(nameComparator);
    prepBinsHtml(binArray);
  };

  var prepBinsHtml = function(binArray){
    var binContainer = d3.select('#name'), bins, lists, items;
    bins = binContainer.selectAll('.bin').data(binArray);
    bins
      .html(function(d){ return '<h4>' + d.name + '</h4>'; });
    bins
      .enter()
        .append('div')
        .attr('class', 'bin span4')
        .html(function(d){ return '<h4>' + d.name + '</h4>'; });
    bins
      .exit()
        .remove();
    items = bins.selectAll('.item').data(function(d){ return d.buildings; });
    items
      .text(function(d){ return d.name_1; })
      .style('display', function(d, i){ return i < 10 ? '' : 'none'; });
    items
      .enter()
        .append('div')
        .attr('class', 'item')
        .text(function(d){ return d.name_1; })
        .style('display', function(d, i){ return i < 10 ? '' : 'none'; })
        .on('click', function(d){
          var url = elbiToUrl(d.elbi);
          if (d3.event.ctrlKey){
            // TODO detect middle click
            window.open(url);
          } else {
            window.document.location.href = url;
          }
        });
    items
      .exit()
        .remove();
  };

  var init = function(data){
    window.data = data; // DEBUG
    _data = data;
    prepNameData(data);

    $('#q').on('keyup', function(){
      var needle = this.value.toUpperCase(),
          filtered = _data.filter(function(d){ return d.name_1.indexOf(needle) !== -1; });
      console.log(filtered.length);
      if (filtered.length < 10) {
        console.log(filtered);
      }
      prepNameData(filtered);
    });
  };

  $.getJSON('/chart/search/data/', init);

})(window, window.jQuery);
