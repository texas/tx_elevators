/*global window, console */

(function(exports, $){
  "use strict";

  var elbiToUrl = function(elbi){
    return $('#elbi-' + elbi + ' > a').prop('href');
  };

  exports.zz = elbiToUrl;

})(window, window.jQuery);
