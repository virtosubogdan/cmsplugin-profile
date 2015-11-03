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
			resizeIframe($('.visible'));
    });

	    $(document).on('click', '.profile-item-actions .delete-profile-item', function(e){
		e.preventDefault();
		profile_id = $(this)[0].attributes["data-profile-id"].value;
		profile_id_prefix = $(this)[0].attributes["data-profile-id-prefix"].value;
		profile_div = $('#' + profile_id_prefix);
		previous_inputs = {};

		jQuery.ajax({
		    type: "POST",
		    url: '/cmsplugin_profile/delete_profile/' + profile_id + "/",
		    success: function (response) {
			if (response['status'] === 'ok') {
			    profile_div.remove();
			} else {
			    alert("Could not delete profile!");
			}
		    },
		    error: function (response) {
			alert("Could not delete profile!");
		    }
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
			resizeIframe();
    });
	    
    $(document).on('click', '.grid-list .revert-profile-changes', function(e){
			e.preventDefault();

			$(this).closest('.visible').removeClass('visible').closest('.inline-related').removeClass('edit-mode');
			$(this).closest('.grid-list').siblings('.overlay').removeClass('visible');

			$.each(previous_inputs, function(key, value) {
			    $('input[name="' + key + '"]')[0].value = value;
			});
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

		$(document).on('click', '.save-profile', function(e) {
			save_link = $(this);
			profile_grid_id = $("#id_profile_set-__prefix__-profile_plugin").attr('value');
			if (profile_grid_id===undefined)
				return;
			save_btn = e.currentTarget;
			profile_prefix = save_btn.attributes["data-profile-id"].value;
			prefix = "#id_" + profile_prefix + "-";
			id_input = $(prefix + "id")[0];
			if (id_input !== undefined) {
				id = id_input.value
			} else {
				id = ""
			}
			data = {
				"id": id,
				"title": $(prefix + "title")[0].value || "",
				"description": $(prefix + "description")[0].value || "",
				"call_to_action_text": $(prefix + "call_to_action_text")[0].value || "",
				"call_to_action_url": $(prefix + "call_to_action_url")[0].value || "",
				"additional_links_label": $(prefix + "additional_links_label")[0].value || "",
				"image_credit": $(prefix + "image_credit")[0].value || "",
				"thumbnail_image": $(prefix + "thumbnail_image")[0].value || "",
				"detail_image": $(prefix + "detail_image")[0].value || "",
			}
			link_index = 1;
			link_prefix = "#" + profile_prefix + "-links_set-";
			while(link_text=$(link_prefix + link_index + "-text")[0]) {
				link_url=$(link_prefix + link_index + "-url")[0];
				link_target=$(link_prefix + link_index + "-open_action")[0];
				link_delete=$(link_prefix + link_index + "-delete")[0];
				data["link-" + link_index + "-text"] = link_text.value;
				data["link-" + link_index + "-url"] = link_url.value;
				data["link-" + link_index + "-target"] = link_target.value;
				data["link-" + link_index + "-delete"] = link_delete.value;
				link_index ++;
			}
			jQuery.ajax({
				type: "POST",
				url: '/cmsplugin_profile/save_profile/' + profile_grid_id + "/",
				data: data,
				success: function (response) {
					if(response["status"] !== "ok"){
						return;
					}
					if (id_input === undefined) {
						id_input = '<input id="id_' + profile_prefix + '-id" name="' + profile_prefix + '-id" type="hidden" value="' + response["id"] + '">';
						$(id_input).insertBefore($(prefix + "title"));
						profile_new = $(".new-profile-form");
						$(".new-profile-form .inline-related").attr("id", profile_prefix);
						$(".new-profile-form .inline-related").attr("class", "ui-widget inline-related ui-sortable-handle");
						profile_html = profile_new.html();
						profile_new.html("");
						$(profile_html).insertBefore($(".ui-widget.inline-related.empty-form"));
					}
					save_link.closest('.visible').removeClass('visible').closest('.inline-related').removeClass('edit-mode');
					$('.overlay').removeClass('visible');
				},
			});
			resizeIframe();
		});
	});
})(jQuery);
