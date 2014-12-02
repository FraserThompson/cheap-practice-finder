var app = app || {};

function calculateRoute(start, end, callback){
	var request = {
		origin: start,
		destination: end,
		travelMode: google.maps.TravelMode.DRIVING
	};

	app.directionsService.route(request, function(response, status) {
		if (status == google.maps.DirectionsStatus.OK){
			callback(response);
		} else {
			console.log("Failed to calculate route: " + status);
		}
	});
}

app.ExpandedView = Backbone.View.extend({

	template: _.template($('#expanded-template').html()),

	id: 'expanded-view',

	render: function(position) {
		var self = this;
		if (this.model.get('url') == "None supplied"){
			var url = "";
		} else {
			var url = this.model.get('url');
		};
		$(this.el).html(this.template({name: this.model.get('name'), pho: this.model.get('pho'), phone: this.model.get('phone'), url: url, address: this.model.get('address')}));
		var table = $('#backgrid-grid');
		var popout_height = $(this.el).outerHeight();
		var table_pos = table.offset()
		table_pos.top += 28; // to account for the header row
		var popout_top = position.top - popout_height/2;
		if (popout_top < table_pos.top){
			popout_top = table_pos.top;
		};
		if (popout_top + popout_height > (table_pos.top - 28) + table.outerHeight()){
			popout_top = (table_pos.top - 28) + table.outerHeight()-popout_height;
		};
		$(this.el).css({
			position: "absolute",
			top: popout_top + "px",
			left: table_pos.left + table.outerWidth() + "px"
		});
		$(this.el).fadeIn(100, function() {
			self.activateMap(self.model);
		});
		return this;
	},

	activateMap: function(model) {
		var coordinates = model.get("coordinates");
		var domElement = this.$("#map_canvas");

		if (coordinates[0] != 0.000) {
			var mapOptions = {
	          center: {lat: coordinates[0], lng: coordinates[1]},
	          zoom: 14
	        };
	        
	        app.directions = new google.maps.DirectionsRenderer();
			app.map = new google.maps.Map(domElement[0], mapOptions);
			
			calculateRoute(model.get("start"), model.get("end"), function(response) {
				if (response) {
					app.directions.setMap(app.map);
					app.directions.setDirections(response);
				} else {
					var marker = new google.maps.Marker({
						position: {lat: coordinates[0], lng: coordinates[1]},
						map: app.map,
						title: model.get("name")
					});
				}
			});
		}
		else {
			domElement.html("<p style='color:white;'>No map</p>");
		}
	},

	unrender: function() {
		var self = this;
		$(this.el).fadeOut(100, function() {
			$(self.el).remove();
		});
	}
});