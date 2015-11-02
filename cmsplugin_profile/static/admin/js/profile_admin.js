(function($) {
	$(document).ready(function() {
	    previous_inputs = {};

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

		previous_inputs = {};
		prefix = $(this)[0].attributes["data-profile-id"].value;
		$('input[name^="' + prefix + '"]').each(function(index, e) {
		    previous_inputs[$(this).attr("name")] = $(this)[0].value;
		});
	    });
	    $(document).on('click', '.grid-list .close-profile', function(e){
		e.preventDefault();

		$(this).closest('.visible').removeClass('visible').closest('.inline-related').removeClass('edit-mode');
		$(this).closest('.grid-list').siblings('.overlay').removeClass('visible');

		profile = $(this).closest('.ui-widget.inline-related');
		if(profile.attr('id') === "-") {
		    profile.remove();
		}
	    });
	    $(document).on('click', '.grid-list .revert-profile-changes', function(e){
		e.preventDefault();

		$(this).closest('.visible').removeClass('visible').closest('.inline-related').removeClass('edit-mode');
		$(this).closest('.grid-list').siblings('.overlay').removeClass('visible');

		$.each(previous_inputs, function(key, value) {
		    $('input[name="' + key + '"]')[0].value = value;
		});

	    });

	});
})(jQuery);
