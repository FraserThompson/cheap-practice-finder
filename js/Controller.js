var app = app || {};

function SouthNorthOrAuckland(coords){
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

	var aucklandCoords = [
		new google.maps.LatLng(-37.343959089444894, 174.638671875),
		new google.maps.LatLng(-37.08585785263673, 175.4571533203125),
		new google.maps.LatLng(-36.24870331653197, 174.9298095703125),
		new google.maps.LatLng(-36.48314061639212, 174.00146484375)
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
	var aucklandPoly = new google.maps.Polygon({paths: aucklandCoords});

	if (google.maps.geometry.poly.containsLocation(new google.maps.LatLng(coords[0], coords[1]), southIslandPoly)){
		return 0;
	} else if (google.maps.geometry.poly.containsLocation(new google.maps.LatLng(coords[0], coords[1]), aucklandPoly)){
		return 3;
	} else {
		return 1;
	}
}

app.Controller = {

	createViews: function() {
		this.searchView = new app.SearchView();
		this.statusView = new app.StatusView();
		this.tableView = new app.TableView();
		this.footerView = new app.FooterView();
	},

	index: function() {
		this.searchView.setElement($('#search-box')).render();
		$('#new-search-address').focus();
		$('#app').fadeIn(800);
	},

	search: function(model) {
		var self = this;
		app.trigger('status:loading');
		app.Practices.setURL(SouthNorthOrAuckland(model.get('coords')));
		self.tableView.unrender(function() {
			app.Practices.fetch({
				reset: true,
				success: function() {
					self.searchView.setElement($('#search-box')).render();
					self.tableView.model.set(model.toJSON());
					self.tableView.refresh();
					app.trigger('status:clear');
				},
				error: function() {
					console.log("Error fetching Practices from JSON file.");
				}
			});
		});
	}
};


