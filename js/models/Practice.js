var app = app || {};
var failed = 0;

app.directionsService = new google.maps.DirectionsService();

app.PracticeModel = Backbone.DeepModel.extend({
	defaults: {
		name: "default",
		url: "default",
		distance: 0,
		start: [0, 0]
	},

	initialize: function() {
		_.bindAll(this, "getPrice", "getDistance");
	},

	parse: function(response) {
		this.prices = response.prices;
		this.set({end: new google.maps.LatLng(response.coordinates[0], response.coordinates[1])});
		return response;
	},

	getPrice: function(age) {
		if (this.prices.length == 0){
			this.set({price: 1000});
			return;
		}
		
		for (var i = 0; i < this.prices.length - 1; ++i){
			if (age >= this.prices[i].age && age < this.prices[i+1].age){
				break;
			}
		}
		this.set({price: this.prices[i].price});
	},

	getDistance: function(addressCoords) {
		this.set({start: new google.maps.LatLng(addressCoords[0], addressCoords[1])});
		if (this.get("coordinates.0") != 0.000) {
			var distance_between = google.maps.geometry.spherical.computeDistanceBetween(this.get("start"), this.get("end"));
			this.set({distance: distance_between/1000});
		} else {
			failed++;
			console.log("Failed to geocode: " + failed);
		}
	return distance_between/1000;
	}
});