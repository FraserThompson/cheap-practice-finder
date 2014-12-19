var app = app || {};

app.Controller = {

	createViews: function() {
		this.searchView = new app.SearchView();
		this.statusView = new app.StatusView();
		this.tableView = new app.TableView();
		this.footerView = new app.FooterView();
	},

	index: function() {
		this.searchView.setElement($('#search-box')).render();
		$('#new-search-address').focus();
		$('#app').fadeIn(800);
	},

	search: function(model) {
		var self = this;
		app.trigger('status:loading');
		this.tableView.unrender(function() {
			app.Practices.fetch({
				reset: true,
				success: function() {
					self.searchView.setElement($('#search-box')).render();
					self.tableView.model.set(model.toJSON());
					self.tableView.refresh();
					app.trigger('status:clear');
				},
				error: function() {
					console.log("Error fetching Practices from JSON file.");
				}
			});
		});
	}
};


