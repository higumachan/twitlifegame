
cell_size = 20
users = null;
status_list = ["atk", "dif", "spd", "brd", "rep"];

draw_chart = (user) ->
	console.log user;
	d = 
		label: user.screen_name,
		data: [i, user[status]] for status, i in status_list,
	console.log d
	opt = 
		radar:
			show:true
		xaxis:
			ticks:[
				[0,"atk"]
				[1,"dif"]
				[2,"spd"]
				[3,"brd"]
				[4,"rep"]
				]
		yaxis:
			noTicks:10
			showLabels:false
			min:0
			max:10
		grid:
			circular:true
	
	Flotr.draw(document.getElementById("reader"), d, opt);

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
							img = users[point.user_id].image;
							image = new Kinetic.Image({
								image: img,
								x: x * cell_size,
								y: y * cell_size,
								height: cell_size,
								width: cell_size,
							});
							user = users[point.user_id];
							image.on("click", ->
								draw_chart(user);
								for status in status_list
									$("#" + status).text(user[status]);
							);
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

