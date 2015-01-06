var app = app || {};
var SouthOrNorth = function(coords){
	var northIslandCoords = [
		new google.maps.LatLng(-41.689322259970425, 175.3857421875),
		new google.maps.LatLng(-40.563894530665074, 176.63818359375),
		new google.maps.LatLng(-39.75787999202175, 177.1875),
		new google.maps.LatLng(-39.33429742980723, 178.1103515625),
		new google.maps.LatLng(-38.34165619279593, 178.79150390625),
		new google.maps.LatLng(-36.949891786813275, 179.14306640625),
		new google.maps.LatLng(-37.43997405227057, 177.07763671875),
		new google.maps.LatLng(-36.33282808737917, 175.9130859375),
		new google.maps.LatLng(-34.867904962568716, 174.74853515625),
		new google.maps.LatLng(-34.542762387234845, 173.38623046875),
		new google.maps.LatLng(-34.361576287484176, 172.529296875),
		new google.maps.LatLng(-35.101934057246055, 172.265625),
		new google.maps.LatLng(-37.07271048132944, 173.6279296875),
		new google.maps.LatLng(-38.169114135560854, 173.95751953125),
		new google.maps.LatLng(-39.266284422130646, 173.232421875),
		new google.maps.LatLng(-39.89287990029478, 173.56201171875),
		new google.maps.LatLng(-40.413496049701955, 174.08935546875),
		new google.maps.LatLng(-40.94671366508001, 174.55078125),
		new google.maps.LatLng(-41.62365539068639, 174.57275390625),
		new google.maps.LatLng(-41.869560826994544, 175.078125)
	];

	var southIslandCoords = [
		new google.maps.LatLng(-47.50235895196858, 168.7939453125),
		new google.maps.LatLng(-42.261049162113835, 175.341796875),
		new google.maps.LatLng(-41.409775832009544, 174.429931640625),
		new google.maps.LatLng(-40.58058466412763, 174.539794921875),
		new google.maps.LatLng(-40.35491675079059, 171.9580078125),
		new google.maps.LatLng(-45.213003555993964, 165.1904296875),
		new google.maps.LatLng(-48.10743118848038, 166.728515625)
	];

	var southIslandPoly = new google.maps.Polygon({paths: southIslandCoords});
	var northIslandPoly = new google.maps.Polygon({paths: northIslandCoords});

	if (google.maps.geometry.poly.containsLocation(new google.maps.LatLng(coords[0], coords[1]), southIslandPoly)){
		return 0;
	} else if (google.maps.geometry.poly.containsLocation(new google.maps.LatLng(coords[0], coords[1]), northIslandPoly)){
		return 1;
	} else {
		return 2;
	}
};

var PracticesCollection = Backbone.Collection.extend({

	model: app.PracticeModel,
	url: 'data.json',

	initialize: function() {
		_.bindAll(this, 'initializeModels', 'changeRadius', 'fetch', 'parse');;
		this.removed = [];
	},

	parse: function() {
		return this.data;
	},

	fetch: function(options) {
		var self = this;
		var trimmed = [];
		if (SouthOrNorth(options.location)) {
			this.url = 'north.json';
		} else {
			this.url = 'south.json';
		}
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
		this.each (function(model) {
			model.getDistance(addressCoords);
			model.getPrice(age);
		});
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