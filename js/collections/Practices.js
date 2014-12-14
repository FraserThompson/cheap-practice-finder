var app = app || {};

var PracticesCollection = Backbone.Collection.extend({
	model: app.PracticeModel,
	url: "data.json",

	initialize: function() {
		_.bindAll(this, 'initializeModels');
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
		var remove = [];
		this.each (function(model) {
			if (model.getDistance(addressCoords) > distance){
				remove.push(model);
			} else {
				model.getPrice(age);
			}
		});
		this.remove(remove);
	}

	// getListOfPHOs: function() {
	// 	var phoList = {};
	// 	this.each (function(model) {
	// 		if (model.get('pho') in phoList) {
	// 			phoList[model.get('pho')] += 1;
	// 		} else {
	// 			phoList[model.get('pho')] = 1;
	// 		}
	// 	});;
	// 	return phoList;
	// }
});

app.Practices = new PracticesCollection();