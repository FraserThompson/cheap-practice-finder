var app = app || {};
app.ExpandedRows = [];

function addressFromCoords(coords, successCallback, failCallback) {
	var self = this;
	var geocoder = new google.maps.Geocoder();
	var coordsObj = new google.maps.LatLng(coords[0], coords[1])
	var geocoderProper = geocoder.geocode({'latLng': coordsObj}, function (results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			successCallback(results[0].address_components[0].long_name +" "+ results[0].address_components[1].long_name +", "+ results[0].address_components[2].long_name + ", "+results[0].address_components[3].long_name);
		} else {
			console.log("Error geocoding input address from coords: " + status);
			failCallback("Error geocoding input address.");
		}
	});
}

var BackgridExpandableRow = Backgrid.Row.extend({
	events: {
		"mouseenter": "glowToggle",
		"mouseleave": "glowToggle",
		"click": "expandRow"
	},


	initialize: function() {
		app.Practices.on('change', this.removeExpandedView, this);
		BackgridExpandableRow.__super__.initialize.apply(this, arguments);
	},

	glowToggle: function() {
		if (!this.expanded) {
			this.$el.toggleClass('hover-glow');
		}
	},

	expandRow: function() {
		var self = this;
		var time = 0;
		var position = $(this.el).offset();
		// If it's not expanded, expand it. If it is expanded, collapse it.
		this.expanded = !this.expanded;
		// Execute the expanding procedure
		if (this.expanded) {
			this.expandedView = new app.ExpandedView({clickPosition: $(this.el).offset()})
			// If there's another row expanded it should  be collapsed and glowed off
			if (app.ExpandedRows.length > 0){
				app.ExpandedRows[0].$el.toggleClass('hover-glow');
				app.ExpandedRows[0].expandRow();
				time = 150;
			}
			setTimeout(function() {
				app.ExpandedRows[0] = self;
				self.expandedView.model = self.model;
				$('#table-view').after(self.expandedView.render().el);
			}, time);
		// Execute the collapsing procedure
		} else {
			app.ExpandedRows.splice(0, 1);
			this.expandedView.unrender();
		}
	},

	removeExpandedView: function() {
		if(this.expandedView){
			this.expandedView.unrender();
		}
	}
});


var BackgridColumns = [
{
	name: "name",
	label: "Name",
	editable: false,
	sortable: false,
	cell: "string",
},
{
	name: "price",
	label: "Price",
	editable: false,
	sortable: true,
	sortType: "toggle",
	cell: Backgrid.NumberCell.extend({
		render: function() {
				this.$el.empty();

			if (this.model.get(this.column.get('name')) != 1000){
				this.$el.html("$" + this.formatter.fromRaw(this.model.get(this.column.get('name'))));
			} else {
				this.$el.html("Unknown");
			}
			this.delegateEvents();
			return this;
		}
	})
},
{
	name: "distance",
	label: "Distance",
	editable: false,
	sortable: true,
	sortType: "toggle",
	cell: Backgrid.IntegerCell.extend({
		render: function() {
			this.$el.empty();
			if (this.model.get(this.column.get('name'))){
				this.$el.html(this.formatter.fromRaw(this.model.get(this.column.get('name'))));
				this.$el.append("km");
			} else {
				this.$el.html("?");
			}
			this.delegateEvents();
			return this;
		}
	})
}
];

app.TableView = Backbone.View.extend({
	
	el: $("#table-view"),

	radius: 2,

	events: {
		'change #radius-select': 'changeRadius'
	},

	initialize: function() {
		_.bindAll(this, 'render', 'unrender', 'changeRadius');
		this.$el.hide(); //hide everything while we're doing stuff
		this.searchOptions = this.$('#search-options');
		this.backgridGrid = this.$('#backgrid-grid');
		app.Practices.initializeModels(this.model.get('age'), this.model.get('coords'), this.radius);
		app.BackgridGrid = new Backgrid.Grid({
			columns: BackgridColumns,
			row: BackgridExpandableRow,
			collection: app.Practices
		});
		this.searchOptionsView = new app.SearchOptionsView();
		this.render();
	},

	render: function() {
		var self = this;
		app.BackgridGrid.render().sort('price', 'ascending');
		var address = addressFromCoords(this.model.get('coords'), function(address) {
			self.searchOptionsView.address = address;
			self.searchOptions.html(self.searchOptionsView.render().el);
			self.backgridGrid.html(app.BackgridGrid.render().el);
			self.$el.slideDown();
		}, function(message){
			self.searchOptions.html(self.searchOptionsView.renderError(message).el);
			self.$el.slideDown();
		});
		return this;
	},

	unrender: function() {
		this.$el.empty();
	},

	changeRadius: function(e) {
		var self = this;
		this.radius = this.$('#radius-select').val()
		app.Practices.fetch({
			reset: false,
			success: function() {
				app.Practices.initializeModels(self.model.get('age'), self.model.get('coords'), self.radius);
				self.searchOptionsView.setCount();
				app.BackgridGrid.render().sort("price", "ascending");
			},
			error: function() {
				console.log("Error fetching practices from JSON file.");
			}
		});
	}
});