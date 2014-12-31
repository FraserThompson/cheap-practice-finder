var app = app || {};

var InfoView = Backbone.View.extend({

	template: _.template($('#info-template').html()),

	render: function() {
		this.$el.html(this.template());
		return this;
	}
});


app.FooterView = Backbone.View.extend({

	el: $('.footer'),

	events: {
		'click .open': 'renderModal'
	},

	renderModal: function(e) {
		var modal = new Backbone.BootstrapModal({cancelText: false, animate: true, content: new InfoView()}).open();
	}
});

