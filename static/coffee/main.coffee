
cell_size = 20
users = null;

window.onload = ->
	stage = new Kinetic.Stage(
		width: 700,
		height: 700,
		container: "container",
	);
	layer = new Kinetic.Layer();
	stage.add(layer);
	
	setInterval(->
		$.getJSON "/get-field", {id: id++}, (json) ->
			if json != null
				layer.removeChildren();
				field = json.field;
				for row, y in field
					for point, x in row
						if point != null
							console.log point
							img = users[point.user_id].image;
							image = new Kinetic.Image({
								image: img,
								x: x * cell_size,
								y: y * cell_size,
								height: cell_size,
								width: cell_size,
							});
							layer.add(image);
				stage.draw();
	, 1000)

$(document).ready ->
	$.getJSON "/get-users", (json) ->
		users = {};
		for user in json
			user.image = new Image();
			user.image.src = "https://api.twitter.com/1/users/profile_image?size=normal&screen_name=" + user.screen_name;
			users[user._id] = user;

