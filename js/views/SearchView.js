var app = app || {};

$.ajaxSetup({beforeSend: function(xhr){
  if (xhr.overrideMimeType)
  {
    xhr.overrideMimeType("application/json");
  }
}
});

function coordsFromAddress(address, successCallback, failCallback) {
	var self = this;
	var geocoder = new google.maps.Geocoder();
	var geocoderProper = geocoder.geocode({'address': address}, function (results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			successCallback(results[0].geometry.location);
		} else {
			failCallback("Invalid input address.")
		}
	});
}

app.SearchView = Backbone.View.extend({

	template: _.template($('#search-template').html()),
	
	events: {
		'keypress #new-search-address': 'setAddress',
		'keypress #new-search-age': 'setAge',
	},

	initialize: function(){
		_.bindAll(this, 'render', 'setAddress', 'setAge');
		this.model = new app.SearchQueryModel();
	},

	render: function(){
		var self = this;
		var statusView = new app.StatusView();
		$(this.el).html(this.template());
		statusView.setElement($('#search-status')).render();
		this.address_input = this.$('#new-search-address');
		this.age_input = this.$('#new-search-age');
		var autocomplete = new google.maps.places.Autocomplete(document.getElementById('new-search-address'), {
			types: ['geocode'],
			componentRestrictions: {country: 'nz'}
		});
		google.maps.event.addListener(autocomplete, 'place_changed', function() {
			self.setAddress({keyCode: 13})
		});
	},

	setAddress: function(e){
		app.trigger('status:clear');
		if (e.keyCode != 13) return;
		if (!this.address_input.val()) return;
		var self = this;
		this.address = this.address_input.val();
		self.address_input.fadeOut(200, function() {
			self.address_input.val('');
			coordsFromAddress(self.address, function(coords){
				self.model.set({coords: coords.lat() + "," + coords.lng()});
				self.age_input.fadeIn(200).focus()
			}, function(message) {
				self.address_input.fadeIn(200).focus();
				app.trigger('status:error', {errorMessage: 'Invalid address.'})
				return;
			});
		});

	},

	setAge: function(e){
		app.trigger('status:clear');
		if (e.keyCode != 13) return;
		if (!this.age_input.val()) return;
		if (!$.isNumeric(this.age_input.val())){
			app.trigger('status:error', {errorMessage: 'Invalid age.'})
			return;
		};
		var self = this;
		this.model.set({age: this.age_input.val()});
		this.age_input.fadeOut(800)
		this.age_input.val('');
		app.ActualRouter.navigate(
          'search/coords=' + this.model.get('coords') + '&age=' +  this.model.get('age') + '&rad=2',
          {trigger: true });
	}
});