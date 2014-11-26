var app = app || {};

app.SearchOptionsView = Backbone.View.extend({

	template: _.template($('#search-options-template').html()),

	address: "error!",

	render: function() {
		$(this.el).html(this.template({address: this.address}));
		this.setCount();
		return this;
	},

	setCount: function() {
		this.$("#count").html(app.Practices.length);
	},

	renderError: function(message) {
		var template = _.template($('#error-template').html())
		$(this.el).html(template({message: message}));
		return this;
	}
});