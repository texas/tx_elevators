/*global window, navigator, console, google */

// django csrf setup
// https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
(function($){
  "use strict";
  // using jQuery
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = $.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
  }

  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
              // Send the token to same-origin, relative URLs only.
              // Send the token only if the method warrants CSRF protection
              // Using the CSRFToken value acquired earlier
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
})(window.jQuery);

// maps
(function(exports, $){
  "use strict";
  var $container = $('#nav-map-container'),
      map,
      homePin,
      buildingMarkers = [],
      debug = $('body').data('debug');

  var initMap = function(center){
    var mapOptions = {
          zoom: 14,
          mapTypeControl: false,
          streetViewControl: false,
          center: center,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
    map = new google.maps.Map($container[0], mapOptions);
    $('#recenter').click(function(){
      var center = map.getCenter(),
          position = {coords:{
            latitude: center.lat(),
            longitude: center.lng()
          }};
      window.getClosestBuildings(position);
    });
  };

  var load = function(centerLatLng, buildings){
    var center = new google.maps.LatLng(
          centerLatLng.latitude,
          centerLatLng.longitude);
    var pinColor = "FFFF00";
    var pinImage = new google.maps.MarkerImage(
          "http://chart.apis.google.com/chart?chst=d_map_pin_icon&chld=home|" + pinColor,
          new google.maps.Size(21, 34),
          new google.maps.Point(0,0),
          new google.maps.Point(10, 34));
    var pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
        new google.maps.Size(40, 37),
        new google.maps.Point(0, 0),
        new google.maps.Point(12, 35));

    if (!map) {
      initMap(center);
    }

    if (!homePin){
      homePin = new google.maps.Marker({
        position: center,
        draggable: true,
        map: map,
        icon: pinImage,
        shadow: pinShadow
      });
      google.maps.event.addDomListener(homePin, 'dragend', function(evt){
        // this: marker
        var newLocation = evt.latLng;
            position = {coords:{
              latitude: newLocation.lat(),
              longitude: newLocation.lng()
            }};
        console.log("drag ended", position.coords);
        window.getClosestBuildings(position);
      });
    } else {
      homePin.setPosition(center);
    }

    if (buildings){
      var building,
          position,
          buildingMarker,
          bounds = new google.maps.LatLngBounds();
      pinColor = "FE7569";
      buildingMarkers.forEach(function(x){ x.setMap(null); });
      buildingMarkers = [];
      $.each(buildings, function(i, building){
        position = new google.maps.LatLng(building.latitude, building.longitude);

        pinImage = new google.maps.MarkerImage(
          "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" +
            String.fromCharCode(65 + i) + "|" + pinColor,
          new google.maps.Size(21, 34),
          new google.maps.Point(0,0),
          new google.maps.Point(10, 34));

        buildingMarker = new google.maps.Marker({
          position: position,
          map: map,
          icon: pinImage,
          shadow: pinShadow,
          title: building.name_1 + ' '  + building.address_1
        });
        if (debug){
          // enable map pin correction
          buildingMarker.setDraggable(true);
          google.maps.event.addDomListener(buildingMarker, 'dragend', function(evt){
            var newLocation = evt.latLng;
                position = {coords:{
                  latitude: newLocation.lat(),
                  longitude: newLocation.lng()
                }};
            $.post('/building/' + building.elbi + '/', position, function(data){
              console.log(data);
            });
          });
        }
        buildingMarkers.push(buildingMarker);
        bounds.extend(position);
      });
      map.fitBounds(bounds);
    }
  };

  // exports
  exports.loadMap = load;

})(window, window.jQuery);

// app
(function(exports, $){
  "use strict";

  var store;

  var storeData = function(data){
    store = data;
    console.log(store.length);
    exports.store = store;
    $(window).trigger('storeAvailable');
  };

  $.getJSON('/chart/locator/data/', storeData);


  var searchZip = function(zip_code){
    var searchZipFilter = function(x){
      return x.zip_code == zip_code;
    };
    return store.filter(searchZipFilter);
  };


  // distance approximators
  /** Converts numeric degrees to radians */
  if (!Number.prototype.toRad){
    Number.prototype.toRad = function(){
      return this * Math.PI / 180;
    };
  }

  // http://www.movable-type.co.uk/scripts/latlong.html
  var distance = {
    R: 63741,  // kilometers
    haversine: function(lat1, lng1, lat2, lng2){
      var dLat = (lat2-lat1).toRad();
      var dLon = (lng2-lng1).toRad();
      lat1 = lat1.toRad();
      lat2 = lat2.toRad();

      var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2);
      var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      return distance.R * c;
    },
    spherical: function(lat1, lng1, lat2, lng2){
      lat1 = lat1.toRad();
      lat2 = lat2.toRad();
      lng1 = lng1.toRad();
      lng2 = lng2.toRad();
      return Math.acos(Math.sin(lat1)*Math.sin(lat2) +
        Math.cos(lat1) * Math.cos(lat2) *
        Math.cos(lng2 - lng1)) * distance.R;
    },
    pythagorean: function(lat1, lng1, lat2, lng2){
      lat1 = lat1.toRad();
      lng1 = lng1.toRad();
      lat2 = lat2.toRad();
      lng2 = lng2.toRad();
      var x = (lng2 - lng1) * Math.cos((lat1 + lat2) / 2),
          y = lat2 - lat1;
      return Math.sqrt(x * x + y * y) * distance.R;
    },
    magic: function(lat1, lng1, lat2, lng2){
      return (Math.abs(lat1 - lat2) + Math.abs(lng1 - lng2)) * distance.R;
    }
  };


  var closestBuildings = function(lat, lng){
    var metric = distance.spherical;
    // go ahead and sort in place.
    store.sort(function(a, b){
      // TODO make a lookup table?
      return metric(lat, lng, a.latitude, a.longitude) - metric(lat, lng, b.latitude, b.longitude);
    });
    return store.slice(0, 10);
  };


  // hook up UI
  // Get the url for a building based on server-side url pattern
  var buildingToUrl = function(building){
    return '/building/' + building.elbi + '/';
  };

  var gotPosition = function(position){
    var lat = position.coords.latitude,
        lng = position.coords.longitude;
    var $container = $('#nearest').empty(),
        buildings = closestBuildings(lat, lng);
    $.each(buildings, function(idx, building){
      $container.append('<li>' +
        '<a href="' + buildingToUrl(building) + '">' + building.name_1 + '</a>, ' +
        building.address_1 + ', ' +
        building.city +
        '</li>');
    });

    window.loadMap(position.coords, buildings);
  };

  $('#locate').on('click', function(){
    navigator.geolocation.getCurrentPosition(gotPosition);
  });

  $(window).on('storeAvailable', function(){
    var data = $('#building-data').data('building');
    if (data && data.latitude){
      gotPosition({
          coords:{
            latitude: data.latitude,
            longitude: data.longitude
          }
      });
    } else {
      navigator.geolocation.getCurrentPosition(gotPosition);
    }
  });


  // exports
  // exports.searchZip = searchZip;
  // exports.d = distance;
  exports.getClosestBuildings = gotPosition;

})(window, window.jQuery);


// chart loader
(function(exports, $){
  var charts = [];
  $('div.chart').each(function(){
    var $this = $(this),
        ar = 1.618,
        width = $this.width(),
        height = Math.floor(width / ar),
        src = $this.attr('data-src');
    var options = {
      ar: ar
    };
    $this.html(
      '<iframe class="chart" src="' + src +
      '" frameborder="0" scrolling=no width="100%" height="' + height +
      '"</iframe>'
    ).data('chartOptions', options);
    charts.push($this);
  });
  $(window).on('resize', function(){
    $.each(charts, function(i, $this){
      // TODO add delay
      var options = $this.data('chartOptions'),
          width = $this.width(),
          height = Math.floor(width / options.ar);
      $this.children('iframe').height(height);
    });
  });
})(window, window.jQuery);
