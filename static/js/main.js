(function() {
  var cell_size, users;

  cell_size = 20;

  users = null;

  window.onload = function() {
    var layer, stage;
    stage = new Kinetic.Stage({
      width: 700,
      height: 700,
      container: "container"
    });
    layer = new Kinetic.Layer();
    stage.add(layer);
    return setInterval(function() {
      return $.getJSON("/get-field", {
        id: id++
      }, function(json) {
        var field, image, img, point, row, x, y, _len, _len2;
        if (json !== null) {
          layer.removeChildren();
          field = json.field;
          for (y = 0, _len = field.length; y < _len; y++) {
            row = field[y];
            for (x = 0, _len2 = row.length; x < _len2; x++) {
              point = row[x];
              if (point !== null) {
                console.log(point);
                img = users[point.user_id].image;
                image = new Kinetic.Image({
                  image: img,
                  x: x * cell_size,
                  y: y * cell_size,
                  height: cell_size,
                  width: cell_size
                });
                layer.add(image);
              }
            }
          }
          return stage.draw();
        }
      });
    }, 1000);
  };

  $(document).ready(function() {
    return $.getJSON("/get-users", function(json) {
      var user, _i, _len, _results;
      users = {};
      _results = [];
      for (_i = 0, _len = json.length; _i < _len; _i++) {
        user = json[_i];
        user.image = new Image();
        user.image.src = "https://api.twitter.com/1/users/profile_image?size=normal&screen_name=" + user.screen_name;
        _results.push(users[user._id] = user);
      }
      return _results;
    });
  });

}).call(this);
