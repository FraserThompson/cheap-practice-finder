app.StatusView = Backbone.View.extend({

	el: $('#search-status'),

	errorTemplate: _.template($('#error-template').html()),

	infoTemplate: _.template($('#info-template').html()),

	initialize: function() {
		this.listenTo(app, 'status:loading', this.startLoading);
		this.listenTo(app, 'status:clear', this.empty);
		this.listenTo(app, 'status:error', this.displayError);
	},

	startLoading: function() {
		$(this.el).html('<h4>Loading...</h4>').addClass('animated fadeIn').show();
		return this;
	},

	empty: function() {
		var self = this;
		$(this.el).slideUp(400, function() {
			$(self.el).empty();
		})
	},

	displayError: function(e) {
		$(this.el).html(this.errorTemplate({message: e.errorMessage})).hide().slideDown();
	}
});