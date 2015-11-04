(function($) {
    $(document).ready(function() {

	function resizeIframe(toResizeTo) {
	    var insideIframe = (window.location != window.parent.location) ? true : false;
	    if (!insideIframe) { return; }

	    var documentHeight = $('body').outerHeight(true);

	    if (toResizeTo) {
  		documentHeight = Math.max($('body').outerHeight(true),
  	    				  toResizeTo.outerHeight(true));
	    }

	    var margin = 20;
	    var _jQuery = window.parent.jQuery || window.parent.$ || (window.parent.django && window.parent.django.jQuery);
	    _jQuery(window.frameElement).css('height', (documentHeight + margin) + 'px');
 	};

	function store_input_data(prefix) {
	    $('input[name^="' + prefix + '"]').each(function(index, e) {
		previous_inputs[$(this).attr("name")] = $(this)[0].value;
	    });
	}

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
	    store_input_data(prefix);
	    resizeIframe($('.visible'));
	});

	$(document).on('click', '.profile-item-actions .delete-profile-item', function(e){
	    e.preventDefault();
	    profile_id_prefix = $(this)[0].attributes["data-profile-id-prefix"].value;
	    profile_div = $('#' + profile_id_prefix)[0];
	    profile_div.style['display'] = "none";
	    $('#id_' + profile_id_prefix + '-DELETE')[0].checked = true;
	});

	$(document).on('click', '.grid-list .close-profile', function(e){
	    e.preventDefault();

	    $(this).closest('.visible').removeClass('visible').closest('.inline-related').removeClass('edit-mode');
	    $(this).closest('.grid-list').siblings('.overlay').removeClass('visible');

	    profile = $(this).closest('.ui-widget.inline-related');
	    if(profile.attr('id') === "-") {
		profile.remove();
	    } else {
		$.each(previous_inputs, function(key, value) {
		    $('input[name="' + key + '"]')[0].value = value;
		});
	    }
	    resizeIframe();
	});

	$(document).on('click', '.grid-list .done-profile', function(e){
	    e.preventDefault();

	    $(this).closest('.visible').removeClass('visible').closest('.inline-related').removeClass('edit-mode');
	    $(this).closest('.grid-list').siblings('.overlay').removeClass('visible');

	    prefix = $(this)[0].attributes["data-profile-id-prefix"].value;
	    last_inputs = $.extend({}, previous_inputs);
	    store_input_data(prefix);
	    if (last_inputs != previous_inputs) {
		$("#warning_unsaved")[0].style.display = "block";
	    }

	    resizeIframe();
	});

	$("#add_new_profile").click(function(e) {
	    var self = this;
	    new_form_index = $('.inline-related').length -1;
	    profile_grid_id = $("#id_profile_set-__prefix__-profile_plugin").attr('value');
	    url = '/cmsplugin_profile/new_profile/' + new_form_index + '/';
	    if (profile_grid_id !== undefined)
				url += "?profilegrid_id=" + profile_grid_id;
	    jQuery.ajax({
		url: url,
		success: function (response) {
		    $('#profile_set-group-grid .new-profile-form').addClass('visible').append(response);
		    $('.overlay').addClass('visible');
		    total = $('#id_profile_set-TOTAL_FORMS')[0];
					total.value = parseInt(total.value) + 1;
		},
		error: function (response) {
		},
		complete: function(response) {
		    resizeIframe($('.visible'));
		}
	    });
	});

	$(document).on('click', '.add-profile-link', function(e) {
	    link = e.currentTarget;
	    prefix = link.attributes["data-prefix"].value;
	    current = parseInt(link.attributes["data-current"].value);
	    next_link = $("#"+prefix+current+"container")[0];
	    if(next_link != undefined) {
		next_link.style.display="block";
		link.attributes["data-current"].value=current+1;
	    }
	    resizeIframe($(this).closest('.visible'));
	});
    });
})(jQuery);
