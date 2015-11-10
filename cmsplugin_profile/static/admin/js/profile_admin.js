(function($) {
    $(document).ready(function() {
        initial_title = $("#id_title")[0].value;
        initial_description = $("#id_description")[0].value;
        initial_show_title = $("#id_show_title_on_thumbnails")[0].checked;
        profile_changed = false;

        function update_show_unsaved_warning() {
            current_title = $("#id_title")[0].value;
            current_description = $("#id_description")[0].value;
            current_show_title = $("#id_show_title_on_thumbnails")[0].checked;

            has_unsaved_changes = profile_changed || current_title != initial_title ||
                current_description != initial_description ||
                current_show_title != initial_show_title;

            $("#warning_unsaved")[0].style.display = has_unsaved_changes ? "block" : "none";
        }

        function isEmpty(field) {
            return field.find('input[type="text"], textarea').val() == '' ? true : false;
        }

        function addErrorClass(field) {
            field.find('input[type="text"], textarea').addClass('error');
        }

        function removeErrorClass(field) {
            field.find('input[type="text"], textarea').removeClass('error');
        }

        function removeAllErrorClasses() {
            $('.has-error, .error').each(function() {
                $(this).removeClass('has-error').removeClass('error');
            });
        }

        function checkValidLinks() {
            $('.profile-add-links .form-row').removeClass('mandatory has-error');
            $('.profile-add-links .form-row input[type="text"]').removeClass('error');

            $('.profile-add-links').each(function() {
                var self = $(this);
                $(this).find('input[type="text"]').each(function() {
                    if ($(this).val().length) {
                        self.find('.form-row').addClass('mandatory');
                    }
                });
            });
        }

        function validateProfile(form) {
            var mandatoryFields = form.find('.mandatory');
            var valid = true;

            mandatoryFields.each(function(idx, elem) {
                if (isEmpty($(elem))) {
                    if ($(elem).parent('.profile-image-panel').length) {
                        $(elem).parent('.profile-image-panel').addClass('has-error');
                    } else {
                        $(elem).addClass('has-error');
                    }
                    addErrorClass($(elem));
                    valid = false;
                } else {
                    removeErrorClass($(elem));
                    $(elem).removeClass('has-error');
                    $(elem).parent('.profile-image-panel').removeClass('has-error');
                }
            });
            return valid;
        }

        function resizeIframe(toResizeTo) {
            var insideIframe = (window.location != window.parent.location) ? true : false;
            if (!insideIframe) {
                return;
            }

            var documentHeight = $('body').outerHeight(true);

            if (toResizeTo) {
                documentHeight = Math.max($('body').outerHeight(true),
                    toResizeTo.outerHeight(true));
            }

            var margin = 20;
            $(window.frameElement).css('height', (documentHeight + margin) + 'px');

            // anchoring on the top of the iframe
            // the classic version (with <a id="anchor">) does not work here due to iframe
            window.parent.$("body").animate({scrollTop: $(window.frameElement).offset().top}, 'fast');
        };

        function store_input_data(prefix) {
            $('input[name^="' + prefix + '"]').each(function(index, e) {
                input = $(this);
                if (input.attr("type") === "checkbox") {
                    type = "checkbox";
                    value = input[0].checked;
                } else {
                    type = "value";
                    value = input.attr("value");
                }
                previous_inputs[input.attr("id")] = [type, value];
            });

            $('textarea[name^="' + prefix + '"]').each(function(index, e) {
                previous_inputs[$(this).attr("id")] = ["value", $(this)[0].value];
            });

            // Save the whole html, must be saved over the normal input values for images
            $.each(['thumbnail_image', 'detail_image'], function(index, image_name) {
                element = $("#id_" + prefix + "-" + image_name);
                html = element.closest("div.profile-image-panel").html();
                previous_inputs[element.attr("id")] = ["image_html", html];
            });
        }

        function restore_input_data() {
            $.each(previous_inputs, function(key, data) {
                type = data[0];
                value = data[1];
                element = $("#" + key);
                if (type === "checkbox") {
                    element[0].checked = value;
                } else if (type === "image_html") {
                    element.closest("div.profile-image-panel").html(value);
                } else {
                    element[0].value = value;
                }
            });
        }

        previous_inputs = {};

        $(document).on("change", "#id_title", function(e) {
            update_show_unsaved_warning();
        });

        $(document).on("change", "#id_description", function(e) {
            update_show_unsaved_warning();
        });

        $(document).on("change", "#id_show_title_on_thumbnails", function(e) {
            update_show_unsaved_warning();
        });

        $(".grid-list").sortable({
            items: "> .inline-related",
            cancel: ".edit-mode",
            update: function(event, ui) {
                $('.order_field input').each(function(i) {
                    $(this).attr('value', i + 1)
                });
            }
        });

        $(document).on('click', '.profile-item-actions .edit-profile-item', function(e) {
            e.preventDefault();
            $(this).parent('.profile-item-actions').siblings().addClass('visible').closest('.inline-related').addClass('edit-mode');
            $(this).closest('.grid-list').siblings('.overlay').addClass('visible');

            previous_inputs = {};
            prefix = $(this)[0].attributes["data-profile-id"].value;
            store_input_data(prefix);
            resizeIframe($('.visible'));
        });

        $(document).on('click', '.profile-item-actions .delete-profile-item', function(e) {
            e.preventDefault();
            profile_id_prefix = $(this)[0].attributes["data-profile-id-prefix"].value;
            profile_div = $('#' + profile_id_prefix)[0];
            profile_div.style['display'] = "none";
            $('#id_' + profile_id_prefix + '-DELETE')[0].checked = true;
        });

        $(document).on('click', '.grid-list .close-profile', function(e) {
            e.preventDefault();

            $(this).closest('.visible').removeClass('visible').closest('.inline-related').removeClass('edit-mode');
            $(this).closest('.grid-list').siblings('.overlay').removeClass('visible');

            profile = $(this).closest('.ui-widget.inline-related');
            if (profile.attr('id') === "-") {
                profile.remove();
            } else {
                restore_input_data();
            }
            removeAllErrorClasses();

            resizeIframe();
        });

        $(document).on('click', '.grid-list .done-profile', function(e) {
            e.preventDefault();
            checkValidLinks();

            if (validateProfile($(this).closest('.visible'))) {
                $(this).closest('.visible').removeClass('visible').closest('.inline-related').removeClass('edit-mode');
                $(this).closest('.grid-list').siblings('.overlay').removeClass('visible');

                prefix = $(this)[0].attributes["data-profile-id-prefix"].value;
                last_inputs = $.extend({}, previous_inputs);
                store_input_data(prefix);
                if (last_inputs != previous_inputs) {
                    profile_changed = true;
                    update_show_unsaved_warning();
                }

                profile_preview = $("#" + prefix);
                new_profile_container = profile_preview.closest(".new-profile-form");
                if (new_profile_container !== undefined && new_profile_container !== null) {
                    profile_html = new_profile_container.html();
                    $(profile_html).insertBefore($(".ui-widget.inline-related.empty-form"));
                    profile_preview = $("#" + prefix);
                    profile_preview[0].className = "ui-widget inline-related complete";
                }

                new_image_url = $("#id_" + prefix + "-thumbnail_image_link_to_file")[0].href;
                profile_preview[0].style.backgroundImage = "url(" + new_image_url + ")";
                resizeIframe();

            }

        });

        $("#add_new_profile").click(function(e) {
            var self = this;
            new_form_index = $('.inline-related').length - 1;
            profile_grid_id = $("#id_profile_set-__prefix__-profile_plugin").attr('value');
            url = '/cmsplugin_profile/new_profile/' + new_form_index + '/';
            if (profile_grid_id !== undefined)
                url += "?profilegrid_id=" + profile_grid_id;
            jQuery.ajax({
                url: url,
                success: function(response) {
                    $('#profile_set-group-grid .new-profile-form').addClass('visible').append(response);
                    $('.overlay').addClass('visible');
                    total = $('#id_profile_set-TOTAL_FORMS')[0];
                    total.value = parseInt(total.value) + 1;
                },
                error: function(response) {},
                complete: function(response) {
                    resizeIframe($('.visible'));
                }
            });
        });

        $(document).on('click', '.add-profile-link', function(e) {
            link = e.currentTarget;
            prefix = link.attributes["data-prefix"].value;
            current = parseInt(link.attributes["data-current"].value);
            next_link = $("#" + prefix + current + "container")[0];
            if (next_link != undefined) {
                next_link.style.display = "block";
                link.attributes["data-current"].value = current + 1;
                is_last_link = $("#" + prefix + (current + 1) + "container")[0] === undefined;
                if (is_last_link) {
                    $(this).closest('p')[0].style.display = "none";
                }
            }
            resizeIframe($(this).closest('.visible'));
        });
    });
})(jQuery);
