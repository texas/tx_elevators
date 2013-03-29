/*global console */
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
  if (typeof(Number.prototype.toRad) === "undefined") {
    Number.prototype.toRad = function() {
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
      return this.R * c;
    },
    spherical: function(lat1, lng1, lat2, lng2){
      return Math.acos(Math.sin(lat1)*Math.sin(lat2) +
        Math.cos(lat1) * Math.cos(lat2) *
        Math.cos(lng2 - lng1)) * this.R;
    },
    pythagorean: function(lat1, lng1, lat2, lng2){
      var x = (lng2 - lng1) * Math.cos((lat1 + lat2) / 2),
          y = lat2 - lat1;
      return Math.sqrt(x * x + y * y) * this.R;
    },
    magic: function(lat1, lng1, lat2, lng2){
      return (Math.abs(lat1 - lat2) + Math.abs(lng1 - lng2)) * this.R;
    }
  };

  exports.searchZip = searchZip;
  exports.d = distance;

})(window, window.jQuery);
// "76104"
