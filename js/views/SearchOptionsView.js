var app = app || {};

app.SearchOptionsView = Backbone.View.extend({

	el: this.$('#search-options'),

	template: _.template($('#search-options-template').html()),

	address: "error!",

	initialize: function() {
		_.bindAll(this, 'setRadius', 'setCount', 'render');
		this.listenTo(app.Practices, 'add remove reset', this.setCount);
	},

	render: function() {
		$(this.el).html(this.template({address: this.address}));
		if (this.address.split(' ')[this.address.split(' ').length - 1] == 'Christchurch'){
			app.trigger('status:error', {errorMessage: 'Limited data for Christchurch. Try <a href="http://www.pegasus.health.nz">http://www.pegasus.health.nz/<a>.'});
		};
		this.setCount();
		return this;
	},

	setCount: function() {
		this.$("#count").html(app.Practices.length);
		//this.$("#phocount").html(_.size(app.Practices.getListOfPHOs()));
	},

	setRadius: function(radius) {
		this.$('#radius-select').val(radius);
	}
});