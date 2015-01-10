var app = app || {};
var failed = 0;

app.directionsService = new google.maps.DirectionsService();

app.PracticeModel = Backbone.DeepModel.extend({
	idAttribute: 'name',
	defaults: {
		name: "default",
		url: "default",
		distance: 0,
		start: [0, 0]
	},

	initialize: function() {
		_.bindAll(this, "getPrice");
	},

	parse: function(response) {
		this.prices = response.prices;
		return response;
	},

	getPrice: function(age) {
		if (!this.prices || this.prices.length == 0){
			this.set({price: 1000});
			return;
		}
		
		for (var i = 0; i < this.prices.length - 1; ++i){
			if (age >= this.prices[i].age && age < this.prices[i+1].age){
				break;
			}
		}
		this.set({price: this.prices[i].price});
		if (this.prices[i].price == 999){
			return -1;
		}
	}
});