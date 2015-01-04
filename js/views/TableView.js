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
<<<<<<< HEAD
		"mouseenter": "glowToggle",
		"mouseleave": "glowToggle",
		"click": "expandRow"
	},


	initialize: function() {
		this.listenTo(app.Practices, 'change', this.removeExpandedView, this);
		this.listenTo(app.Practices, 'backgrid:refresh', this.removeExpandedView, this);
		BackgridExpandableRow.__super__.initialize.apply(this, arguments);
	},

	glowToggle: function() {
		if (!this.expanded) {
			this.$el.toggleClass('hover-glow');
		}
	},

	expandRow: function() {
		// If it's not expanded, expand it. If it is expanded, collapse it.
		this.expanded = !this.expanded;
		var self = this;
		var time = 0;
		// Execute the expanding procedure
		if (this.expanded) {
			this.$el.addClass('hover-glow');
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
=======
		'click': 'expandRow'
	},

	initialize: function() {
		_.bindAll(this, 'expandRow', 'removeExpandedView');
		this.listenTo(Backbone, 'backgrid:refresh backgrid:expand', this.removeExpandedView);
		BackgridExpandableRow.__super__.initialize.apply(this, arguments);
	},

	expandRow: function() {
		var self = this;
		if (!this.expandedView) {
			Backbone.trigger('backgrid:expand');
			this.expandedView = new app.ExpandedView({clickPosition: $(this.el).position()})
			self.expandedView.model = self.model;
			this.$el.addClass('hover-glow');
			self.$el.after(self.expandedView.render().el);
			this.expandedView.setCSSPosition();
		} else {
			this.removeExpandedView();
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
		}
	},

	removeExpandedView: function() {
		if(this.expandedView){
			this.expandedView.unrender();
<<<<<<< HEAD
=======
			this.$el.toggleClass('hover-glow');
			this.expandedView = 0;
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
		}
	}
});


var BackgridColumns = [
{
	name: "name",
	label: "Name",
	editable: false,
	sortable: false,
<<<<<<< HEAD
	cell: "string",
=======
	cell: "string"
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
},
{
	name: "price",
	label: "Price",
	editable: false,
	sortable: true,
	sortType: "toggle",
	cell: Backgrid.NumberCell.extend({
		render: function() {
<<<<<<< HEAD
				this.$el.empty();

			if (this.model.get(this.column.get('name')) != 1000){
				this.$el.html("$" + this.formatter.fromRaw(this.model.get(this.column.get('name'))));
			} else {
=======
			this.$el.empty();
			if (this.model.get(this.column.get('name')) != 1000){
				this.$el.html("$" + this.formatter.fromRaw(this.model.get(this.column.get('name'))));
			} else if (this.model.get(this.column.get('name')) == 1000){
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
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
<<<<<<< HEAD
	
	el: $("#table-view"),

	radius: 2,

=======

	model: new app.SearchQueryModel(),
	
	el: $("#table-view"),

>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
	events: {
		'change #radius-select': 'changeRadius'
	},

	initialize: function() {
<<<<<<< HEAD
		_.bindAll(this, 'render', 'unrender', 'changeRadius');
		this.$el.hide(); //hide everything while we're doing stuff
		this.searchOptions = this.$('#search-options');
		this.backgridGrid = this.$('#backgrid-grid');
		app.Practices.initializeModels(this.model.get('age'), this.model.get('coords'), this.radius);
		app.BackgridGrid = new Backgrid.Grid({
			columns: BackgridColumns,
			row: BackgridExpandableRow,
			collection: app.Practices,
			emptyText: "None found."
		});
		this.searchOptionsView = new app.SearchOptionsView();
		this.render();
	},

	refresh: function() {
		app.Practices.initializeModels(this.model.get('age'), this.model.get('coords'), this.radius);
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
=======
		this.$el.hide();
		_.bindAll(this, 'render', 'changeRadius', 'refresh');
		app.isMobile = window.matchMedia("only screen and (max-width: 760px)");
		this.searchOptionsElement = this.$('#search-options');
		this.backgridGridElement = this.$('#backgrid-grid');
		this.BackgridGrid = new Backgrid.Grid({
			columns: BackgridColumns,
			row: BackgridExpandableRow,
			collection: app.Practices,
			emptyText: "None found.",
			className: 'backgrid table-hover'
		});
		this.backgridGridElement.html(this.BackgridGrid.render().el);
		this.searchOptionsView = new app.SearchOptionsView();
	},

	render: function(callback) {
		var self = this;
		var address = addressFromCoords(this.model.get('coords'), function(address) {
			self.searchOptionsView.address = address;
			self.searchOptionsView.render();
			self.searchOptionsView.setRadius(self.model.get('radius'));
			self.BackgridGrid.render().sort('price', 'ascending');
			self.$el.slideDown();
			callback();
		}, function(message){
			app.trigger('status:error', {errorMessage: message})
			self.$el.slideDown();
			callback();
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
		});
		return this;
	},

<<<<<<< HEAD
	unrender: function() {
		this.$el.empty();
=======
	unrender: function(callback) {
		$(this.el).fadeOut(200, function() {
			callback();
		});
	},

	refresh: function(callback) {
		var self = this;
		app.Practices.initializeModels(this.model.get('age'), this.model.get('coords'), function() {
			app.Practices.changeRadius(self.model.get('radius'), function() {
				self.render(function() {
					callback();
				});
			});
		});
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
	},

	changeRadius: function(e) {
		var self = this;
<<<<<<< HEAD
		this.radius = this.$('#radius-select').val()
		app.Practices.fetch({
			reset: true,
			success: function() {
				app.Practices.initializeModels(self.model.get('age'), self.model.get('coords'), self.radius);
				self.searchOptionsView.setCount();
				app.BackgridGrid.render().sort("price", "ascending");
			},
			error: function() {
				console.log("Error fetching practices from JSON file.");
			}
=======
		this.model.set({'radius': this.$('#radius-select').val()});
		app.Practices.changeRadius(self.model.get('radius'), function() {
			self.BackgridGrid.render().sort('price', 'ascending');
			app.ActualRouter.navigate(
	          'search/coords=' + self.model.get('coords') + '&age=' +  self.model.get('age') + '&rad=' + self.model.get('radius'),
	          {trigger: false });
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
		});
	}
});