  var _data;

  function stackData(data){
    var newData = [],
        lookup = {};

    // uhhh I'm sure d3 has this built in somewhere. I don't know where though.
    // this is sort of like layouts.stack
    var key, counter;
    for (var i = 0; i < data.length; i++){
      key = data[i].year_installed + ':' + data[i].floors;
      if (!lookup[key]) {
        lookup[key] = 0;
      }
      lookup[key]++;
    }
    var bits;
    $.each(lookup, function(key, value){
      bits = key.split(':');
      newData.push({
        year_installed: parseInt(bits[0], 10),
        floors: parseInt(bits[1], 10),
        value: value
      });
  });
    return newData;
  }

  function chart(data){

    data = stackData(data);

    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = $(window).width(),
        height = $(window).height(),
        plotWidth = width - margin.left - margin.right,
        plotHeight = height - margin.top - margin.bottom;

    var x = d3.scale.linear().range([0, plotWidth]),
        y = d3.scale.linear().range([plotHeight, 0]);

    var svg = d3.select('#chart').append('svg')
      .attr('viewBox', [0, 0, width, height].join(" "))
      .attr('preserveAspectRatio', 'xMinYMin meet')
      .attr('width', '100%')
      .attr('height', '100%');

    var plot = svg.append('g')
          .attr('class', 'plot')
          .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    xAttrName = 'year_installed',
        yAttrName = 'floors',
        xAccessor = function(d){ return d[xAttrName]; },
        yAccessor = function(d){ return d[yAttrName]; },
        vAccessor = function(d){ return d.value; },
        xCoord = function(d){ return x(d[xAttrName]); },
        yCoord = function(d){ return y(d[yAttrName]); };

    // x.domain(d3.extent(data, xAccessor));
    x.domain([1913, 2013]);
    y.domain([0, d3.max(data, yAccessor)]).nice();


    // colors
    // colors from colorbrewer diverging scheme
    var colorExtent = d3.extent(data, vAccessor);
    var color = d3.scale.log()
      .range(['rgb(44, 123, 182)', 'rgb(255, 255, 191)', 'rgb(215, 25, 28)'])
      .domain([colorExtent[0], (1 / 3 * (colorExtent[0] + colorExtent[1])), colorExtent[1]]);
    window.zz = color;

    var barWidth = x(x.domain()[0] + 1),  // 1 unit wide
        barHeight = y(y.domain()[1] - 1);  // 1 unit high
    plot.selectAll('.dot').data(data)
      .enter().append('rect')
        .attr('class', 'dot')
        .attr('x', xCoord)
        .attr('y', yCoord)
        .attr('stroke-width', 0)
        .attr('width', barWidth)
        .attr('height', barHeight)
        .style('fill', function(d){ return color(d.value); });

    var xAxis = d3.svg.axis()
          .scale(x)
          .orient("bottom")
          .tickFormat(function(d){ return d; }),
        yAxis = d3.svg.axis()
          .scale(y)
          .orient("left");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + margin.left + "," + (margin.top + plotHeight) + ")")
        .call(xAxis)
      .append("text")
        .attr("class", "label")
        .attr("x", plotWidth>>1)
        .attr("y", 26)
        .style("text-anchor", "end")
        .text("year");

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .call(yAxis)
      .append("text")
        .attr("class", "label")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("floors");
  }

  $.getJSON('data/', function(response){
    _data = response;
    chart(_data);
  });
