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

	tagName: 'tr',

	id: 'expanded-view',

	render: function() {
		var self = this;	
		$(this.el).html(this.template({pho: this.model.get('pho'), phone: this.model.get('phone'), url: this.model.get('url'), address: this.model.get('address')}));
		$(this.el).find('p').slideDown(400);
		$(this.el).find('div').slideDown(400);
		// Wait until the canvas is visible before trying to render the map 
		setTimeout(function() { ;
			self.activateMap(self.model);
		}, 410);
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
			google.maps.event.trigger(this.map, 'resize');
		}
		else {
			domElement.html("<p style='color:white;'>No map</p>");
		}
	},

	unrender: function() {
		var self = this;
		$(this.el).find('p').slideUp(300);
		$(this.el).find('div').slideUp(300);
		setTimeout(function() {
			$(self.el).remove();
		}, 300);
	}
});