var app = app || {};

function calculateRoute(start, end, callback){
	var request = {
		origin: start,
		destination: end,
		travelMode: google.maps.TravelMode.DRIVING
	};

	app.directionsService.route(request, function(response, status) {
		if (status == google.maps.DirectionsStatus.OK){
			callback(response);
		} else {
			console.log("Failed to calculate route: " + status);
		}
	});
}

app.ExpandedView = Backbone.View.extend({

	template: _.template($('#expanded-template').html()),

	id: 'expanded-view',

	tagName: function() {
		if (app.isMobile.matches) {
			return 'tr';
		} else {
			return 'div';
		}
	},

	clickPosition: 0,

	table: $('#backgrid-grid'),

	initialize: function(options) {
		_.bindAll(this, 'render', 'unrender', 'setCSSPosition', 'activateMap');
		this.listenTo(app.Practices, 'backgrid:refresh', this.unrender);
		if (app.isMobile.matches) {
			this.mobile = 1;
	        this.template = _.template($('#expanded-template-mobile').html());
	    };
		this.clickPosition = options.clickPosition;
		$(window).on('resize', this.setCSSPosition);
	},

	setCSSPosition: function() {
		if (!this.mobile){
			var popout_height = 520 + 28 //CHANGE THIS IF YOU CHANGE IT IN THE CSS BECAUSE CHROME 
			var table_pos = this.table.position();
			var table_height = this.table.outerHeight()
			var table_width = this.table.outerWidth()
			table_pos.top += 28; // to account for the header row
			var popout_top = this.clickPosition.top - popout_height/2;
			if (popout_top < table_pos.top) {
				popout_top = table_pos.top;
			}
			else if (popout_top + popout_height > (table_pos.top - 28) + table_height){
				popout_top = (table_pos.top - 28) + table_height-popout_height;
			};
			$(this.el).css({
				position: "absolute",
				top: popout_top + "px",
				left: table_pos.left + table_width + "px"
			});
		} else {
			return;
		}
	},

	render: function() {
		var self = this;
		if (this.model.get('url') != ""){
			var url = this.model.get('url');
		} else {
			var url = "https://www.google.co.nz/#q=" + this.model.get('name');
		};
		$(this.el).html(this.template({name: this.model.get('name'), pho: this.model.get('pho'), phone: this.model.get('phone'), url: url, address: this.model.get('address')}));
		this.setCSSPosition();
		if (this.mobile){
			this.$el.css({
				'height': 'auto',
				'padding': '0px'
			});
		}
		$(this.el).fadeIn(200, function() {
			self.activateMap(self.model);
		});
		return this;
	},

	activateMap: function(model) {
		var coordinates = model.get("coordinates");
		var domElement = this.$("#map_canvas");

		if (coordinates[0] != 0.000) {
			var mapOptions = {
	          center: {lat: coordinates[0], lng: coordinates[1]},
	          zoom: 14
	        };
	        
	        app.directions = new google.maps.DirectionsRenderer();
			app.map = new google.maps.Map(domElement[0], mapOptions);
			
			calculateRoute(model.get("start"), model.get("end"), function(response) {
				if (response) {
					app.directions.setMap(app.map);
					app.directions.setDirections(response);
				} else {
					var marker = new google.maps.Marker({
						position: {lat: coordinates[0], lng: coordinates[1]},
						map: app.map,
						title: model.get("name")
					});
				}
			});
		}
		else {
			domElement.html("<p style='color:white;'>No map</p>");
		}
	},

	unrender: function() {
		var self = this;
		this.$("#map_canvas").remove();
		$(window).off('resize', this.setCSSPosition)
		$(this.el).fadeOut(200, function() {
			$(self.el).remove();
			this.remove();
		});
	}
});