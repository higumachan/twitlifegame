(function() {
  var cell_size, draw_chart, status_list, users;

  cell_size = 20;

  users = null;

  status_list = ["atk", "dif", "spd", "brd", "rep"];

  draw_chart = function(user) {
    var d, i, opt, status;
    console.log(user);
    d = {
      label: user.screen_name,
      data: (function() {
        var _len, _results;
        _results = [];
        for (i = 0, _len = status_list.length; i < _len; i++) {
          status = status_list[i];
          _results.push([i, user[status]]);
        }
        return _results;
      })()
    };
    console.log(d);
    opt = {
      radar: {
        show: true
      },
      xaxis: {
        ticks: [[0, "atk"], [1, "dif"], [2, "spd"], [3, "brd"], [4, "rep"]]
      },
      yaxis: {
        noTicks: 10,
        showLabels: false,
        min: 0,
        max: 10
      },
      grid: {
        circular: true
      }
    };
    return Flotr.draw(document.getElementById("reader"), d, opt);
  };

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
        var field, image, img, point, row, user, x, y, _len, _len2;
        if (json !== null) {
          layer.removeChildren();
          field = json.field;
          for (y = 0, _len = field.length; y < _len; y++) {
            row = field[y];
            for (x = 0, _len2 = row.length; x < _len2; x++) {
              point = row[x];
              if (point !== null) {
                img = users[point.user_id].image;
                image = new Kinetic.Image({
                  image: img,
                  x: x * cell_size,
                  y: y * cell_size,
                  height: cell_size,
                  width: cell_size
                });
                user = users[point.user_id];
                image.on("click", function() {
                  var status, _i, _len3, _results;
                  draw_chart(user);
                  _results = [];
                  for (_i = 0, _len3 = status_list.length; _i < _len3; _i++) {
                    status = status_list[_i];
                    _results.push($("#" + status).text(user[status]));
                  }
                  return _results;
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
