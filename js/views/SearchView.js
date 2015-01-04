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

<<<<<<< HEAD
	el: $('#search-view'),
	template: _.template($('#search-template').html()),
	errorTemplate: _.template($('#error-template').html()),
	
	events: {
		'keypress #new-search-address': 'setAddress',
		'keypress #new-search-age': 'setAge',
=======
	model: new app.SearchQueryModel(),

	template: _.template($('#search-template').html()),
	
	events: {
		'keypress #new-search-address': 'setAddress',
		'keypress #new-search-age': 'setAge'
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
	},

	initialize: function(){
		_.bindAll(this, 'render', 'setAddress', 'setAge');
<<<<<<< HEAD
		this.model = new app.SearchQueryModel();
		this.searchStatus = this.$('#search-status');
		this.searchBox = this.$('#search-box');
		this.render();
=======
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
	},

	render: function(){
		var self = this;
<<<<<<< HEAD
		this.searchBox.html(this.template());
		this.address_input = this.$('#new-search-address');
		this.age_input = this.$('#new-search-age');
		this.address_input.focus();
		var autocomplete = new google.maps.places.Autocomplete(document.getElementById('new-search-address'), {
			types: ['geocode'],
=======
		$(this.el).html(this.template()).addClass('animated fadeIn');
		this.address_input = this.$('#new-search-address');
		this.age_input = this.$('#new-search-age');
		var autocomplete = new google.maps.places.Autocomplete(document.getElementById('new-search-address'), {
		types: ['geocode'],
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
			componentRestrictions: {country: 'nz'}
		});
		google.maps.event.addListener(autocomplete, 'place_changed', function() {
			self.setAddress({keyCode: 13})
		});
<<<<<<< HEAD
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
=======
	},

	setAddress: function(e){
		app.trigger('status:clear');
		if (e.keyCode != 13) return;
		if (!this.address_input.val()) return;
		var self = this;
		this.address = this.address_input.val();
		this.address_input.addClass('animated fadeOut');
		this.address_input.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
			self.address_input.val('').removeClass('animated fadeOut').hide();
			coordsFromAddress(self.address, function(coords){
				self.model.set({coords: [coords.lat(), coords.lng()]});
				self.age_input.addClass('animated fadeIn').show().focus();
			}, function(message) {
				self.address_input.addClass('animated fadeIn').show().focus();
				app.trigger('status:error', {errorMessage: 'Invalid address.'});
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
				return;
			});
		});

	},

	setAge: function(e){
<<<<<<< HEAD
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
          '/search?address=' + this.model.get('coords') + '&age=' +  this.model.get('age'),
          {trigger: true });
	},

	startLoading: function() {
		this.searchStatus.html("<p>Loading...</p>").fadeIn();
	},

	finishLoading: function(callback) {
		this.searchStatus.fadeOut(400, callback);
=======
		app.trigger('status:clear');
		if (e.keyCode != 13) return;
		if (!this.age_input.val()) return;
		if (!$.isNumeric(this.age_input.val())){
			app.trigger('status:error', {errorMessage: 'Invalid age.'})
			return;
		};
		var self = this;
		this.model.set({age: this.age_input.val()});
		this.age_input.val('').addClass('animated fadeOut');
		this.age_input.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
			app.trigger('status:loading');
			self.age_input.removeClass('animated fadeOut').hide();
			app.Controller.search(self.model);
			app.ActualRouter.navigate(
	          'search/coords=' + self.model.get('coords') + '&age=' +  self.model.get('age') + '&rad=2',
	          {trigger: false });
		})
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
	}
});