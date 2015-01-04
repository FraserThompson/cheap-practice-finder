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
<<<<<<< HEAD
		'click .open': 'renderModal',
=======
		'click .open': 'renderModal'
>>>>>>> 10008f5919bb8185173792ae79b35a8a60212386
	},

	renderModal: function(e) {
		var modal = new Backbone.BootstrapModal({cancelText: false, animate: true, content: new InfoView()}).open();
	}
});

