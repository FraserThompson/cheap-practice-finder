var app = app || {};

app.SearchOptionsView = Backbone.View.extend({

<<<<<<< HEAD
=======
	el: this.$('#search-options'),

>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
	template: _.template($('#search-options-template').html()),

	address: "error!",

<<<<<<< HEAD
	render: function() {
		$(this.el).html(this.template({address: this.address}));
		if (this.address.split(' ')[this.address.split(' ').length - 1] == 'Christchurch'){
			this.renderError('Limited data for Christchurch. Try <a href="http://www.pegasus.health.nz">http://www.pegasus.health.nz/<a>.');
=======
	initialize: function() {
		_.bindAll(this, 'setRadius', 'setCount', 'render');
		this.listenTo(app.Practices, 'add remove reset', this.setCount);
	},

	render: function() {
		$(this.el).html(this.template({address: this.address}));
		if (this.address.split(' ')[this.address.split(' ').length - 1] == 'Christchurch'){
			app.trigger('status:error', {errorMessage: 'Limited data for Christchurch. Try <a href="http://www.pegasus.health.nz">http://www.pegasus.health.nz/<a>.'});
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
		};
		this.setCount();
		return this;
	},

	setCount: function() {
		this.$("#count").html(app.Practices.length);
<<<<<<< HEAD
		this.$("#phocount").html(_.size(app.Practices.getListOfPHOs()));
	},

	renderError: function(message) {
		var template = _.template($('#error-template').html())
		$(this.el).html(template({message: message}));
		return this;
=======
		//this.$("#phocount").html(_.size(app.Practices.getListOfPHOs()));
	},

	setRadius: function(radius) {
		this.$('#radius-select').val(radius);
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
	}
});