var app = app || {};

var PracticesCollection = Backbone.Collection.extend({
	model: app.PracticeModel,
	url: "data.json",

	initialize: function() {
		_.bindAll(this, 'getDistances', 'getPrices', 'filterByDistance', 'initializeModels');
		this.sort_key = 'price';
	},

	comparator: function(a, b){
		a = a.get(this.sort_key);
		b = b.get(this.sort_key);
		return a > b ? 1
			: a < b ? -1
			: 0; 
	},

	initializeModels: function(age, addressCoords, distance) {
		this.getPrices(age);
		this.getDistances(addressCoords);
		this.filterByDistance(distance);
	},

	getDistances: function(addressCoords) {
		var self = this;
		this.each (function(model) {
			model.getDistance(addressCoords);
		});
	},

	getPrices: function(age) {
		this.each (function(model) {
			model.getPrice(age);
		});
	},

	filterByDistance: function(distance) {
		var filter = _.filter(this.models, function(item) {
			return item.get('distance') < distance;
		});
		this.reset(filter);
	}
});

app.Practices = new PracticesCollection();