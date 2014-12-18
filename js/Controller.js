var app = app || {};

app.Controller = {

	createViews: function() {
		app.searchView = new app.SearchView();
		app.statusView = new app.StatusView();
		app.tableView = new app.TableView();
		app.footerView = new app.FooterView();
	},

	index: function() {
		app.searchView.setElement($('#search-box')).render();
		$('#new-search-address').focus();
		$('#app').fadeIn(800);
	},

	search: function(model) {
		app.trigger('status:loading');
		app.tableView.unrender(function() {
			app.Practices.fetch({
				reset: true,
				success: function() {
					app.searchView.setElement($('#search-box')).render();
					app.tableView.model.set(model.toJSON());
					app.tableView.refresh();
					app.trigger('status:clear');
				},
				error: function() {
					console.log("Error fetching Practices from JSON file.");
				}
			});
		});
	}
};


