app.StatusView = Backbone.View.extend({

	el: $('#search-status'),

	errorTemplate: _.template($('#error-template').html()),

	infoTemplate: _.template($('#info-template').html()),

	initialize: function() {
		this.listenTo(app, 'status:loading', this.startLoading);
		this.listenTo(app, 'status:clear', this.empty);
		this.listenTo(app, 'status:error', this.displayError);
		this.listenTo(app, 'status:info', this.displayInfo);
	},

	startLoading: function() {
		$(this.el).html('<h4>Loading...</h4>').fadeIn();
		return this;
	},

	empty: function() {
		$(this.el).slideUp(400).empty();
	},

	displayError: function(e) {
		$(this.el).html(this.errorTemplate({message: e.errorMessage})).hide().slideDown();
	},

	displayInfo: function(e) {
		var self = this;
		$(this.el).html(this.infoTemplate({message: e.infoMessage})).hide().slideDown(function() {
			self.empty();
		});
	}
});