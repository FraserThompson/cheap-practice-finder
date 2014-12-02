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
		'search/:address/:age': 'search'
	},

	search: function(address, age){	
		$('#app').show();
		$('#table-view').fadeOut();
		if (!app.footerView){
			app.footerView = new app.FooterView();
		}
		$('#expanded-view').remove();
		app.searchView = new app.SearchView();
		app.searchView.startLoading();
		app.Practices.fetch({
			reset: true,
			success: function() {
				app.searchView.finishLoading(function() {
					var searchQuery = new app.SearchQueryModel({age: age, coords: address.split(",")});
					app.tableView = new app.TableView({model: searchQuery});
				});
			},
			error: function() {
				console.log("Error fetching Practices from JSON file.");
			}
		});
	},

	index: function() {
		if (app.tableView) {
			app.tableView.unrender();
		}
		$('#app').fadeIn(800);
		app.searchView = new app.SearchView();
		app.footerView = new app.FooterView();
	}
});

app.ActualRouter = new app.Router();
Backbone.history.start();