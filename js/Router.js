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
		$('#table-view').fadeOut();
		app.statusView || (app.statusView = new app.StatusView());
		app.searchView || (app.searchView = new app.SearchView());
		app.trigger('status:loading');
		app.Practices.fetch({
			reset: false,
			success: function() {
				app.searchView.setElement($('#search-box')).render();
				var searchQuery = new app.SearchQueryModel({age: age, coords: address.split(","), radius: rad});
				if (!app.tableView){
					app.tableView = new app.TableView({model: searchQuery});
				} else {
					app.tableView.model = searchQuery;
					app.tableView.refresh();
				};
			},
			error: function() {
				console.log("Error fetching Practices from JSON file.");
			}
		});
		app.trigger('status:clear');
	},

	index: function() {
		app.statusView = new app.StatusView();
		app.searchView = new app.SearchView();
		app.footerView = new app.FooterView();
		app.trigger('status:clear');
		app.searchView.setElement($('#search-box')).render();
		$('#new-search-address').focus();
		$('#app').fadeIn(800);
	}
});

_.extend(app, Backbone.Events);
app.ActualRouter = new app.Router();
Backbone.history.start();