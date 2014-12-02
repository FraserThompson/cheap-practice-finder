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

	el: $('#search-view'),
	template: _.template($('#search-template').html()),
	errorTemplate: _.template($('#error-template').html()),
	
	events: {
		'keypress #new-search-address': 'setAddress',
		'keypress #new-search-age': 'setAge',
	},

	initialize: function(){
		_.bindAll(this, 'render', 'setAddress', 'setAge');
		this.model = new app.SearchQueryModel();
		this.searchStatus = this.$('#search-status');
		this.searchBox = this.$('#search-box');
		this.render();
	},

	render: function(){
		var self = this;
		this.searchBox.html(this.template());
		this.address_input = this.$('#new-search-address');
		this.age_input = this.$('#new-search-age');
		this.address_input.focus();
		var autocomplete = new google.maps.places.Autocomplete(document.getElementById('new-search-address'), {
			types: ['geocode'],
			componentRestrictions: {country: 'nz'}
		});
		google.maps.event.addListener(autocomplete, 'place_changed', function() {
			self.setAddress({keyCode: 13})
		});
		return this;
	},

	setAddress: function(e){
		if (e.keyCode != 13) return;
		if (!this.address_input.val()) return;
		var self = this;
		this.searchStatus.slideUp(100);
		this.address = this.address_input.val();
		self.address_input.fadeOut(200, function() {
			self.address_input.val('');
			coordsFromAddress(self.address, function(coords){
				self.model.set({coords: coords.lat() + "," + coords.lng()});
				self.age_input.fadeIn(200).focus()
			}, function(message) {
				self.address_input.fadeIn(200).focus();
				self.searchStatus.html(self.errorTemplate({message: "That address doesn't exist."})).hide().slideDown();
				return;
			});
		});

	},

	setAge: function(e){
		if (e.keyCode != 13) return;
		if (!this.age_input.val()) return;
		if (!$.isNumeric(this.age_input.val())){
			this.searchStatus.html(this.errorTemplate({message: "Please enter a valid age."})).hide().slideDown();
			return;
		};
		this.searchStatus.slideUp(100);
		var self = this;
		this.model.set({age: this.age_input.val()});
		this.age_input.fadeOut(800)
		this.age_input.val('');
		app.ActualRouter.navigate(
          '/search/' + this.model.get('coords') + '/' +  this.model.get('age'),
          {trigger: true });
	},

	startLoading: function() {
		this.searchStatus.html("<p>Loading...</p>").fadeIn();
	},

	finishLoading: function(callback) {
		this.searchStatus.fadeOut(400, callback);
	}
});