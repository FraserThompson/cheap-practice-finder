var app = app || {};

app.SearchQueryModel = Backbone.Model.extend({
	defaults: {
		coords: 5,
		age: 2
	}
});