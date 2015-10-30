(function($) {
	$(document).ready(function() {

		$( ".grid-list" ).sortable({
		  items: "> .inline-related",
		  cancel: ".edit-mode",
		  update: function(event, ui) {
		  	$('.order_field input').each(function(i){$(this).attr('value', i+1)});
		  }
		});
		
		$(document).on('click', '.profile-item-actions .edit-profile-item', function(e){
			e.preventDefault();
			$(this).parent('.profile-item-actions').siblings().addClass('visible').closest('.inline-related').addClass('edit-mode');
			$(this).closest('.grid-list').siblings('.overlay').addClass('visible');
		});
		$(document).on('click', '.grid-list .close-profile', function(e){
			e.preventDefault();
			$(this).closest('.visible').removeClass('visible').closest('.inline-related').removeClass('edit-mode');
			$(this).closest('.grid-list').siblings('.overlay').removeClass('visible');
		});
	});
})(jQuery);
