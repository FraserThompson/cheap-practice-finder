var app = app || {};

var PracticesCollection = Backbone.Collection.extend({

	model: app.PracticeModel,
	url: 'data.json',

	initialize: function() {
		_.bindAll(this, 'initializeModels', 'changeRadius', 'fetch', 'parse');
		this.removed = [];
		this.data = $.getJSON(this.url);
	},

	parse: function() {
		alert('before parseing:' + this.data.length)
		return this.data;
	},

	fetch: function(options) {
		var self = this;
		var trimmed = [];
		this.removed = [];
		$.getJSON(this.url, function(data) {
			$.each(data, function(key, val) {
				var distance_between = google.maps.geometry.spherical.computeDistanceBetween(new google.maps.LatLng(val['coordinates'][0], val['coordinates'][1]), new google.maps.LatLng(options.location[0], options.location[1]));
				if ((distance_between/1000) <= 15){
					trimmed.push(val);
				}
			});
			self.data = trimmed;
		});
		return Backbone.Collection.prototype.fetch.call(this, options)
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
			if (model.get('distance') >= distance){
				remove_these.push(model);
			}
		});
		this.removed = remove_these;
		this.remove(remove_these);
		callback();
	},

	initializeModels: function(age, addressCoords, callback) {
		var self = this;
		var remove_these = [];
		this.each (function(model) {
			model.getDistance(addressCoords);
			if (model.getPrice(age) == -1){
				remove_these.push(model);
			};
		});
		this.remove(remove_these);
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