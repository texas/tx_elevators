/*global window, console, d3 */

(function(exports, $){
  "use strict";

  var _data, currentBinAccessor;

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

  var binAccessors = {
    buildingName: function(d){
      var key = d.name_1[0];
      if ($.isNumeric(key)){
        return "0&ndash;9";
      }
      return key.toUpperCase();
    },
    city: function(d){ return d.city; },
    zip: function(d){ return d.zip_code; }
  };

  var prepNameData = function(data){
    var bins = binData(data, currentBinAccessor);

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
    var _ = d3.format(","),
        binTitleHTML = function(d){ return '<h4>' + d.name + ' <small>(' + _(d.buildings.length) + ')</small></h4>'; },
        itemClass = function(d, i) { return 'item' + (i < 10 ? '' : ' overflow'); },
        itemTitle = function(d){ return d.address_1 + ', ' + d.city + ', TX ' + d.zip_code; },
        itemText = function(d){ return d.name_1; };
    var binContainer = d3.select('#name'), bins, lists, items;
    bins = binContainer.selectAll('.bin').data(binArray);
    bins
      .attr('class', 'bin span4')
      .html(binTitleHTML);
    bins
      .enter()
        .append('div')
        .attr('class', 'bin span4')
        .html(binTitleHTML);
    bins
      .exit()
        .remove();
    items = bins.selectAll('.item').data(function(d){ return d.buildings; });
    items
      .attr('class', itemClass)
      .attr('title', itemTitle)
      .text(itemText);
    items
      .enter()
        .append('div')
        .attr('class', itemClass)
        .attr('title', itemTitle)
        .text(itemText)
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

  var processSearch = function(evt){
      var needle = this.value.toUpperCase(),
          filtered = _data.filter(function(d){ return d.name_1.indexOf(needle) !== -1; });
      console.log(filtered.length);
      if (filtered.length < 10) {
        console.log(filtered);
      }
      prepNameData(filtered);
  };

  var init = function(data){
    $('#name').removeClass('loading');
    _data = data;

    var $methods = $('#search-container ul.nav > li');
    $methods.find('a').click(function(e){
      e.preventDefault();
      var $this = $(this);
      $this.parent().addClass('active').siblings().removeClass('active');

      var method = $this.attr('href').split('#')[1];
      currentBinAccessor = binAccessors[method];
      processSearch.call(document.getElementById('q'));
    });
    var method = $methods.filter('.active').find('a').attr('href').split('#')[1];
    currentBinAccessor = binAccessors[method];

    prepNameData(data);

    $('#q')
      .on('keydown', function(e){ if (e.which == 27) { this.value = ''; }})
      .on('keyup', processSearch);

    $('#show-all').click(function(){
      $('#name div.bin').toggleClass('show-all');
    });
  };
  var url = $('script:last').prev('a').attr('href');
  $.getJSON(url, init);

})(window, window.jQuery);
