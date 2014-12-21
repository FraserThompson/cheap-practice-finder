var app = app || {};

var PracticesCollection = Backbone.Collection.extend({
	model: app.PracticeModel,
	url: 'data.json',

	initialize: function() {
		_.bindAll(this, 'initializeModels', 'changeRadius');
		this.sort_key = 'price';
		this.removed = [];
	},

	setURL: function(SouthNorthOrAuckland) {
		if(SouthNorthOrAuckland == 0){
			this.url = 'si.json';
			console.log('south island data');
		} else if (SouthNorthOrAuckland == 1){
			this.url = 'ni.json';
			console.log('north island data');
		} else {
			this.url = 'auckland.json';
			console.log('auckland data');
		}
	},

	comparator: function(a, b){
		a = a.get(this.sort_key);
		b = b.get(this.sort_key);
		return a > b ? 1
			: a < b ? -1
			: 0; 
	},

	changeRadius: function(distance, callback) {
		var self = this;
		// There's most likely a better way to do all this...
		if (this.removed.length != 0){
			this.removed.forEach(function(model) {
				self.push(model);
			})
		}
		var remove_these = [];
		this.each (function(model) {
			if (model.get('distance') > distance){
				remove_these.push(model);
			}
		});
		this.removed = JSON.parse(JSON.stringify(remove_these));
		this.remove(remove_these);
		callback();
	},

	initializeModels: function(age, addressCoords, callback) {
		var remove = [];
		this.each (function(model) {
			if (model.getDistance(addressCoords) > 15){
				remove.push(model);
			} else {
				model.getPrice(age);
			}
		});
		this.remove(remove);
		callback();
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