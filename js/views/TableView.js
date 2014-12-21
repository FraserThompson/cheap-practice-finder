var app = app || {};
app.ExpandedRows = [];

function addressFromCoords(coords, successCallback, failCallback) {
	var self = this;
	var geocoder = new google.maps.Geocoder();
	var coordsObj = new google.maps.LatLng(coords[0], coords[1])
	var geocoderProper = geocoder.geocode({'latLng': coordsObj}, function (results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			console.log(results[0].address_components[4].long_name);
			successCallback(results[0].address_components[0].long_name +" "+ results[0].address_components[1].long_name +", "+ results[0].address_components[2].long_name + ", "+results[0].address_components[3].long_name);
		} else {
			console.log("Error geocoding input address from coords: " + status);
			failCallback("Error geocoding input address.");
		}
	});
}

var BackgridExpandableRow = Backgrid.Row.extend({
	events: {
		'mouseenter': 'glowToggle',
		'mouseleave': 'glowToggle',
		'click': 'expandRow'
	},

	initialize: function() {
		_.bindAll(this, 'glowToggle', 'expandRow', 'removeExpandedView');
		this.listenTo(app.Practices, 'change', this.removeExpandedView, this);
		BackgridExpandableRow.__super__.initialize.apply(this, arguments);
	},

	glowToggle: function() {
		if (!this.expanded) {
			this.$el.toggleClass('hover-glow');
		}
	},

	expandRow: function() {
		this.expanded = !this.expanded;
		var self = this;
		var time = 0;
		if (this.expanded) {
			this.$el.addClass('hover-glow');
			this.expandedView = new app.ExpandedView({clickPosition: $(this.el).position()})
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
			} else if (this.model.get(this.column.get('name')) == 1000{
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

	model: new app.SearchQueryModel(),
	
	el: $("#table-view"),

	events: {
		'change #radius-select': 'changeRadius'
	},

	initialize: function() {
		this.$el.hide();
		_.bindAll(this, 'render', 'changeRadius', 'refresh');
		this.searchOptionsElement = this.$('#search-options');
		this.backgridGridElement = this.$('#backgrid-grid');
		this.BackgridGrid = new Backgrid.Grid({
			columns: BackgridColumns,
			row: BackgridExpandableRow,
			collection: app.Practices,
			emptyText: "None found."
		});
		this.backgridGridElement.html(this.BackgridGrid.render().el);
		this.searchOptionsView = new app.SearchOptionsView();
	},

	render: function() {
		var self = this;
		var address = addressFromCoords(this.model.get('coords'), function(address) {
			self.searchOptionsView.address = address;
			self.searchOptionsView.render();
			self.searchOptionsView.setRadius(self.model.get('radius'));
			self.BackgridGrid.render().sort('price', 'ascending');
			self.$el.slideDown();
		}, function(message){
			app.trigger('status:error', {errorMessage: message})
			self.$el.slideDown();
		});
		return this;
	},

	unrender: function(callback) {
		$(this.el).fadeOut(200, function() {
			callback();
		});
	},

	refresh: function() {
		var self = this;
		app.Practices.initializeModels(this.model.get('age'), this.model.get('coords'), function() {
			app.Practices.changeRadius(self.model.get('radius'), function() {
				self.render();
			});
		});
	},

	changeRadius: function(e) {
		var self = this;
		this.model.set({'radius': this.$('#radius-select').val()});
		app.Practices.changeRadius(self.model.get('radius'), function() {
			self.BackgridGrid.render().sort('price', 'ascending');
			app.ActualRouter.navigate(
	          'search/coords=' + self.model.get('coords') + '&age=' +  self.model.get('age') + '&rad=' + self.model.get('radius'),
	          {trigger: false });
		});
	}
});