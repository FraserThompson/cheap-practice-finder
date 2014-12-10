var app = app || {};

app.SearchOptionsView = Backbone.View.extend({

	template: _.template($('#search-options-template').html()),

	address: "error!",

	render: function() {
		$(this.el).html(this.template({address: this.address}));
		if (this.address.split(' ')[this.address.split(' ').length - 1] == 'Christchurch'){
			this.renderError('Limited data for Christchurch. Try <a href="http://www.pegasus.health.nz">http://www.pegasus.health.nz/<a>.');
		};
		this.setCount();
		return this;
	},

	setCount: function() {
		this.$("#count").html(app.Practices.length);
		this.$("#phocount").html(_.size(app.Practices.getListOfPHOs()));
	},

	renderError: function(message) {
		var template = _.template($('#error-template').html())
		$(this.el).html(template({message: message}));
		return this;
	}
});