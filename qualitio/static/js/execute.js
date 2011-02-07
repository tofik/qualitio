function render_application_view(type, node, view) {
  $('#application-view').load("/execute/ajax/"+type+"/"+node+"/"+view+"/");
}

hash.main = function() {
  object_plain_id = hash.node.split("_")[0]
  render_application_view(hash.object, object_plain_id, hash.view);
}

$(function() {
  $("#application-tree").jstree({
    "plugins" : [ "themes", "json_data", "ui", "cookies","types"],
    "json_data" : {
      "ajax" : {
        "url" : "ajax/get_children",
        "data" : function (n) {
          return {
            id : n.attr ? n.attr("id").split("_")[0] : 0, //get only the id from {id}_{type_name}
            type: n.attr ? n.attr("rel") : "testrundirectory"
          };
        }
      }
    },
    "types" : {
      "valid_children" : [ "testrundirectory"],
      
      "types" : {
        "testrundirectory" : {
          "valid_children" : "all"
        },
        "testrun" : {
          "icon" : {
            "image" : "/static/images/file.png"
          },
        }
      }
    }
  }).bind("select_node.jstree", function (node, data) {
    
    hash.object = data.rslt.obj.attr('rel');
    hash.node = data.rslt.obj.attr("id").split("_")[0];
    if (!hash.view || hash.view == 'new')
      hash.view = 'details';
    hash.update(true);
    
  }).bind("loaded.jstree", function (event, data) {
    if(!window.location.hash)
      $("#application-tree").jstree("select_node",".jstree-last");
  });
  
  hash.init();
});
