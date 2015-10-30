(function($) {
	$(document).ready(function() {

		$( ".grid-list" ).sortable({
		  items: "> .inline-related",
		  update: function(event, ui) {
		  	$('.order_field input').each(function(i){$(this).attr('value', i+1)});
		  }
		});
	
	});
})(jQuery);
