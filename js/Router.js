var app = app || {};

$.ajaxSetup({beforeSend: function(xhr){
  if (xhr.overrideMimeType)
  {
    xhr.overrideMimeType("application/json");
  }
}
});

app.Router = Backbone.Router.extend({

	routes: {
		'': 'index',
		'search/coords=:address&age=:age&rad=:rad': 'search'
	},

	search: function(address, age, rad){
		$('#app').show();
		app.Controller.createViews();
		app.trigger('status:loading');
		app.Controller.search(new app.SearchQueryModel({coords: address.split(','), age: age, radius: rad}));
	},

	index: function() {
		app.Controller.createViews()
		app.Controller.index();
	}
});

_.extend(app, Backbone.Events);
app.ActualRouter = new app.Router();
Backbone.history.start();