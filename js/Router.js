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
		'search?address=:address&age=:age': 'search'
	},

	search: function(address, age){	
		$('#app').show();
		$('#table-view').fadeOut();
		var statusView = new app.StatusView();
		var searchView = new app.SearchView();
		statusView.setElement($('#search-status')).render();
		app.trigger('status:loading');
		app.Practices.fetch({
			reset: true,
			success: function() {
				app.trigger('status:clear');
				searchView.setElement($('#search-box')).render();
				var searchQuery = new app.SearchQueryModel({age: age, coords: address.split(",")});
				if (!tableView){
					var tableView = new app.TableView({model: searchQuery});
				} else {
					tableView.model = searchQuery;
					tableView.radius = 2;
					tableView.refresh();
				};
			},
			error: function() {
				console.log("Error fetching Practices from JSON file.");
			}
		});
	},

	index: function() {
		var searchView = new app.SearchView();
		var footerView = new app.FooterView();
		var statusView = new app.StatusView();
		searchView.setElement($('#search-box')).render();
		statusView.setElement($('#search-status')).render();
		$('#app').fadeIn(800);
	}
});

_.extend(app, Backbone.Events);
app.ActualRouter = new app.Router();
Backbone.history.start();