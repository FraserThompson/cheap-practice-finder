app.StatusView = Backbone.View.extend({

	errorTemplate: _.template($('#error-template').html()),

	initialize: function() {
		this.listenTo(app, 'status:loading', this.startLoading);
		this.listenTo(app, 'status:clear', this.clear);
		this.listenTo(app, 'status:error', this.displayError);
	},

	startLoading: function() {
		$(this.el).html('<h4>Loading...</h4>');
	},

	clear: function() {
		$(this.el).slideUp(400);
	},

	displayError: function(e) {
		$(this.el).html(this.errorTemplate({message: e.errorMessage})).hide().slideDown();
	}
});