/*global navigator, console */
(function(exports, $){
  "use strict";

  var store;

  var storeData = function(data){
    store = data;
    console.log(store.length);
    exports.store = store;
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
    var metric = distance.pythagorean;
    // go ahead and sort in place.
    store.sort(function(a, b){
      // TODO make a lookup table?
      return metric(lat, lng, a.latitude, a.longitude) - metric(lat, lng, b.latitude, b.longitude);
    });
    return store.slice(0, 10);
  };


  // hook up UI
  if (!navigator.geolocation){
    $('body').addClass('no-geolocation');
  }

  // Get the url for a building based on server-side url pattern
  var buildingToUrl = function(building){
    return '/building/' + building.elbi + '/';
  };

  var gotPosition = function(position){
    var lat = position.coords.latitude,
        lng = position.coords.longitude;
    var $container = $('#nearest').empty();
    $.each(closestBuildings(lat, lng), function(idx, building){
      $container.append('<li>' +
        '<a href="' + buildingToUrl(building) + '">' + building.name_1 + '</a>, ' +
        building.address_1 + ', ' +
        building.city +
        '</li>');

    });
  };

  $('#locate').one('click', function(){
    navigator.geolocation.getCurrentPosition(gotPosition);
  });


  // exports
  // exports.searchZip = searchZip;
  // exports.d = distance;
  // exports.c = closestBuildings;

})(window, window.jQuery);
// "76104"
