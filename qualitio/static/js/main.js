// HashController,
// Implementation based on jquery-ui site, try to understand it, don't blame it.
var hash = {
  storedHash: '',
  listen: true,
  interval: null,
  cache: '',

  object : null,
  node : null,
  view : null,

  _start_listening: function() {
    setTimeout(function() {
      hash.listen = true;
    }, 600);
  },

  _stop_listening: function() {
    hash.listen = false;
  },

  _has_changed: function() {
    var locStr = hash.current_hash();
    if(hash._clean(hash.storedHash) != locStr) {
      hash._parse();

      if(hash.listen == true) {
        hash.main();
        hash.post_main();
      }
      hash.storedHash = locStr;
    }
    if(!hash.interval) hash.interval = setInterval(hash._has_changed, 50);
  },

  _parse: function() {
    segments = hash.current_hash().split("/");
    hash.object = segments[0];
    hash.node = segments[1];
    hash.view = segments[2];
  },

  _clean: function(locStr){
    return locStr.replace(/%23/g, "").replace(/[\?#]+/g, "");
  },

  init: function(){
    if (window.location.hash) {
      hash._parse()
      hash.update();
    } else {
      hash.storedHash = '';
    }
    hash._has_changed();
  },

  update: function(refresh) {
    hash.storedHash = hash.to_string();
    window.location.hash = hash.to_string();
    if (refresh) {
      hash.main();
    }
  },

  current_hash: function() {
    return hash._clean(window.location.hash);
  },

  to_string: function() {
    return "#"+[hash.object, hash.node, hash.view].join("/")+"/";
  },

  // Controller view. Will react on every anchor change. Implement your logic here
  main: function() {
    return alert("One function to rule them all, not implemented")
  },

  post_main: function() {
    return 0;
  }
};

var resize_main_window = function() {
  $('#application-view, #application-tree')
    .css('height',
         document.body.clientHeight - 
         $('#header').height() - 
         // because overflow needs to be launched earlier
         2*$('#footer').height());
};

$(document).ready(function() {
  $('#notification').jnotifyInizialize({
    oneAtTime: true
  });

  resize_main_window();
});

$(window).resize(function() {
  resize_main_window();
});


