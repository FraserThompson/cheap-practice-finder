var app = app || {};

app.SearchQueryModel = Backbone.Model.extend({
	defaults: {
		coords: 0,
		age: 0,
		radius: 2
	}
});
