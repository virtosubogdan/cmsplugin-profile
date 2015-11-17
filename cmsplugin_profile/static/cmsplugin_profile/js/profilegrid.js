/*
 * debouncedresize: special jQuery event that happens once after a window resize
 *
 * latest version and complete README available on Github:
 * https://github.com/louisremi/jquery-smartresize/blob/master/jquery.debouncedresize.js
 *
 * Copyright 2011 @louis_remi
 * Licensed under the MIT license.
 */
var $event = $.event,
    $special,
    resizeTimeout;

$special = $event.special.debouncedresize = {
    setup: function() {
        $(this).on("resize", $special.handler);
    },
    teardown: function() {
        $(this).off("resize", $special.handler);
    },
    handler: function(event, execAsap) {
        // Save the context
        var context = this,
            args = arguments,
            dispatch = function() {
                // set correct event type
                event.type = "debouncedresize";
                $event.dispatch.apply(context, args);
            };

        if (resizeTimeout) {
            clearTimeout(resizeTimeout);
        }

        execAsap ?
            dispatch() :
            resizeTimeout = setTimeout(dispatch, $special.threshold);
    },
    threshold: 250
};

// ======================= imagesLoaded Plugin ===============================
// https://github.com/desandro/imagesloaded

// $('#my-container').imagesLoaded(myFunction)
// execute a callback when all images have loaded.
// needed because .load() doesn't work on cached images

// callback function gets image collection as argument
//  this is the container

// original: MIT license. Paul Irish. 2010.
// contributors: Oren Solomianik, David DeSandro, Yiannis Chatzikonstantinou

// blank image data-uri bypasses webkit log warning (thx doug jones)
var BLANK = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==';

$.fn.imagesLoaded = function(callback) {
    var $this = this,
        deferred = $.isFunction($.Deferred) ? $.Deferred() : 0,
        hasNotify = $.isFunction(deferred.notify),
        $images = $this.find('img').add($this.filter('img')),
        loaded = [],
        proper = [],
        broken = [];

    // Register deferred callbacks
    if ($.isPlainObject(callback)) {
        $.each(callback, function(key, value) {
            if (key === 'callback') {
                callback = value;
            } else if (deferred) {
                deferred[key](value);
            }
        });
    }

    function doneLoading() {
        var $proper = $(proper),
            $broken = $(broken);

        if (deferred) {
            if (broken.length) {
                deferred.reject($images, $proper, $broken);
            } else {
                deferred.resolve($images);
            }
        }

        if ($.isFunction(callback)) {
            callback.call($this, $images, $proper, $broken);
        }
    }

    function imgLoaded(img, isBroken) {
        // don't proceed if BLANK image, or image is already loaded
        if (img.src === BLANK || $.inArray(img, loaded) !== -1) {
            return;
        }

        // store element in loaded images array
        loaded.push(img);

        // keep track of broken and properly loaded images
        if (isBroken) {
            broken.push(img);
        } else {
            proper.push(img);
        }

        // cache image and its state for future calls
        $.data(img, 'imagesLoaded', {
            isBroken: isBroken,
            src: img.src
        });

        // trigger deferred progress method if present
        if (hasNotify) {
            deferred.notifyWith($(img), [isBroken, $images, $(proper), $(broken)]);
        }

        // call doneLoading and clean listeners if all images are loaded
        if ($images.length === loaded.length) {
            setTimeout(doneLoading);
            $images.unbind('.imagesLoaded');
        }
    }

    // if no images, trigger immediately
    if (!$images.length) {
        doneLoading();
    } else {
        $images.bind('load.imagesLoaded error.imagesLoaded', function(event) {
            // trigger imgLoaded
            imgLoaded(event.target, event.type === 'error');
        }).each(function(i, el) {
            var src = el.src;

            // find out if this image has been already checked for status
            // if it was, and src has not changed, call imgLoaded on it
            var cached = $.data(el, 'imagesLoaded');
            if (cached && cached.src === src) {
                imgLoaded(el, cached.isBroken);
                return;
            }

            // if complete is true and browser supports natural sizes, try
            // to check for image status manually
            if (el.complete && el.naturalWidth !== undefined) {
                imgLoaded(el, el.naturalWidth === 0 || el.naturalHeight === 0);
                return;
            }

            // cached images don't fire load sometimes, so we reset src, but only when
            // dealing with IE, or image is complete (loaded) and failed manual check
            // webkit hack from http://groups.google.com/group/jquery-dev/browse_thread/thread/eee6ab7b2da50e1f
            if (el.readyState || el.complete) {
                el.src = BLANK;
                el.src = src;
            }
        });
    }

    return deferred ? deferred.promise($this) : $this;
};

var Grid = (function() {

    // list of items
    var $grid = $('#og-grid'),
        // the items
        $items = $grid.children('li'),
        // current expanded item's index
        current = -1,
        // position (top) of the expanded item
        // used to know if the preview will expand in a different row
        previewPos = -1,
        // extra amount of pixels to scroll the window
        scrollExtra = 0,
        // extra margin when expanded (between preview overlay and the next items)
        marginExpanded = 30,
        $window = $(window),
        winsize,
        $body = $('html, body'),
        // transitionend events
        transEndEventNames = {
            'WebkitTransition': 'webkitTransitionEnd',
            'MozTransition': 'transitionend',
            'OTransition': 'oTransitionEnd',
            'msTransition': 'MSTransitionEnd',
            'transition': 'transitionend'
        },
        transEndEventName = transEndEventNames[Modernizr.prefixed('transition')],
        // support for csstransitions
        support = Modernizr.csstransitions,
        // default settings
        settings = {
            minHeight: 650,
            speed: 350,
            easing: 'ease'
        };

    function init(config) {

        // the settings..
        settings = $.extend(true, {}, settings, config);

        // preload all images
        $grid.imagesLoaded(function() {

            // save item´s size and offset
            saveItemInfo(true);
            // get window´s size
            getWinSize();
            // initialize some events
            initEvents();

        });

    }

    // add more items to the grid.
    // the new items need to appended to the grid.
    // after that call Grid.addItems(theItems);
    function addItems($newitems) {

        $items = $items.add($newitems);

        $newitems.each(function() {
            var $item = $(this);
            $item.data({
                offsetTop: $item.offset().top,
                height: $item.height()
            });
        });

        initItemsEvents($newitems);

    }

    // saves the item´s offset top and height (if saveheight is true)
    function saveItemInfo(saveheight) {
        $items.each(function() {
            var $item = $(this);
            $item.data('offsetTop', $item.offset().top);
            if (saveheight) {
                $item.data('height', $item.height());
            }
        });
    }

    function initEvents() {

        // when clicking an item, show the preview with the item´s info and large image.
        // close the item if already expanded.
        // also close if clicking on the item´s cross
        initItemsEvents($items);

        // on window resize get the window´s size again
        // reset some values..
        $window.on( 'debouncedresize', function() {
            scrollExtra = 0;
            previewPos = -1;
            // save item´s offset
            saveItemInfo(true);
            //Preview
            getWinSize();
            var preview = $.data(this, 'preview');

            if (typeof preview != 'undefined') {
                hidePreview();
            }

        });

    }

    function initItemsEvents($items) {
        $items.on('click', 'span.og-close', function() {
            hidePreview();
            return false;
        }).children('a').on('click', function(e) {

            var $item = $(this).parent();
            // check if item already opened
            current === $item.index() ? hidePreview() : showPreview($item);
            return false;

        });
    }

    function getWinSize() {
        winsize = {
            width: $window.width(),
            height: $window.height()
        };
    }

    function showPreview($item) {
        var preview = $.data(this, 'preview'),
            // item´s offset top
            position = $item.data('offsetTop');


        scrollExtra = 0;

        // if a preview exists and previewPos is different (different row) from item´s top then close it
        if (typeof preview != 'undefined') {

            // not in the same row
            if (previewPos !== position) {
                // if position > previewPos then we need to take te current preview´s height in consideration when scrolling the window
                if (position > previewPos) {
                    scrollExtra = preview.height;
                }
                hidePreview();
            }
            // same row
            else {
                preview.update($item);
                return false;
            }

        }

        // update previewPos
        previewPos = position;
        // initialize new preview for the clicked item
        preview = $.data(this, 'preview', new Preview($item));
        // expand preview overlay
        preview.open();

    }

    function hidePreview() {
        current = -1;
        var preview = $.data(this, 'preview');
        preview.close();
        $.removeData(this, 'preview');
    }

    // the preview obj / overlay
    function Preview($item) {
        this.$item = $item;
        this.expandedIdx = this.$item.index();
        this.create();
        this.update();
    }

    Preview.prototype = {
        create: function() {
            // create Preview structure:

            this.$title = $('<h3></h3>');
            this.$description = $('<p></p>');
            this.$href = $('<a href=""></a>');
            this.$additionalLinksLabel = $('<span></span>');
            this.$addLinkA = $('<a href="#" target=""></a>');
            this.$addLinkB = $('<a href="" target=""></a>');
            this.$addLinkC = $('<a href="" target=""></a>');
            this.$addLinkD = $('<a href="" target=""></a>');
            this.$details = $('<div class="og-details"></div>').append(this.$title, this.$description, this.$href);
            this.$bottomDetails = $('<div class="og-bottom-details"></div>').append(this.$additionalLinksLabel, this.$addLinkA, this.$addLinkB, this.$addLinkC, this.$addLinkD);
            this.$fullimageCredit = $('<span class="og-img-credit"></span>');
            this.$loading = $('<div class="og-loading"></div>');
            this.$fullimage = $('<div class="og-fullimg"></div>').append(this.$loading);
            this.$fullimageWrapper = $('<div class="og-fullimg-wrapper"></div>').append(this.$fullimage);
            this.$closePreview = $('<span class="og-close"></span>');
            this.$previewInner = $('<div class="og-expander-inner"></div>').append(this.$closePreview, this.$fullimageWrapper, this.$details, this.$bottomDetails);
            this.$previewEl = $('<div class="og-expander"></div>').append(this.$previewInner);
            // append preview element to the item
            this.$item.append(this.getEl());
            // set the transitions for the preview and the item
            if (support) {
                this.setTransition();
            }
        },
        update: function($item) {

            if ($item) {
                this.$item = $item;
            }

            // if already expanded remove class "og-expanded" from current item and add it to new item
            if (current !== -1) {
                var $currentItem = $items.eq(current);
                $currentItem.removeClass('og-expanded');
                this.$item.addClass('og-expanded');
                // position the preview correctly
                this.positionPreview();
            }

            // update current value
            current = this.$item.index();

            // update preview´s content
            var $itemEl = this.$item.children('a'),
                eldata = {
                    href: $itemEl.attr('href'),
                    largesrc: $itemEl.data('largesrc'),
                    largeimageCredit: $itemEl.data('largeimg-credit'),
                    title: $itemEl.data('title'),
                    description: $itemEl.data('description'),
                    callToActionText: ($itemEl.data('calltoactiontext') ? $itemEl.data('calltoactiontext') : $itemEl.attr('href')),
                    additionalLinksLabel: $itemEl.data('additionallinkslabel'),
                    addLinkTextA: $itemEl.data('addlinktext1'),
                    addLinkUrlA: $itemEl.data('addlinkurl1'),
                    addLinkTargetA: $itemEl.data('addlinktarget1'),
                    addLinkTextB: $itemEl.data('addlinktext2'),
                    addLinkUrlB: $itemEl.data('addlinkurl2'),
                    addLinkTargetB: $itemEl.data('addlinktarget2'),
                    addLinkTextC: $itemEl.data('addlinktext3'),
                    addLinkUrlC: $itemEl.data('addlinkurl3'),
                    addLinkTargetC: $itemEl.data('addlinktarget3'),
                    addLinkTextD: $itemEl.data('addlinktext4'),
                    addLinkUrlD: $itemEl.data('addlinkurl4'),
                    addLinkTargetD: $itemEl.data('addlinktarget4')
                };
            this.$title.html(eldata.title);
            this.$description.html(eldata.description);

            if (eldata.href.length) {
                this.$href.attr('href', eldata.href);
                this.$href.text(eldata.callToActionText);
                this.$href.show();
            } else {
                this.$href.empty();
                this.$href.hide();
            }
            if (eldata.largeimageCredit) {
                this.$fullimageCredit.show().text(eldata.largeimageCredit);
            } else {
                this.$fullimageCredit.hide();
            }
            this.$additionalLinksLabel.html(eldata.additionalLinksLabel);

            var emptyLinks = 0;
            if (eldata.addLinkTextA) {
                this.$addLinkA.show();
                this.$addLinkA.text(eldata.addLinkTextA);
                this.$addLinkA.attr('href', eldata.addLinkUrlA);
                this.$addLinkA.attr('target', eldata.addLinkTargetA);
            } else {
                this.$addLinkA.hide();
                emptyLinks++;
            }

            if (eldata.addLinkTextB) {
                this.$addLinkB.show();
                this.$addLinkB.text(eldata.addLinkTextB);
                this.$addLinkB.attr('href', eldata.addLinkUrlB);
                this.$addLinkB.attr('target', eldata.addLinkTargetB);
            } else {
                this.$addLinkB.hide();
                emptyLinks++;
            }

            if (eldata.addLinkTextC) {
                this.$addLinkC.show();
                this.$addLinkC.text(eldata.addLinkTextC);
                this.$addLinkC.attr('href', eldata.addLinkUrlC);
                this.$addLinkC.attr('target', eldata.addLinkTargetC);
            } else {
                this.$addLinkC.hide();
                emptyLinks++;
            }

            if (eldata.addLinkTextD) {
                this.$addLinkD.show();
                this.$addLinkD.text(eldata.addLinkTextD);
                this.$addLinkD.attr('href', eldata.addLinkUrlD);
                this.$addLinkD.attr('target', eldata.addLinkTargetD);
            } else {
                this.$addLinkD.hide();
                emptyLinks++;
            }
            if (emptyLinks == 4 && !eldata.additionalLinksLabel) {
                this.$bottomDetails.hide();
            }
            else {
                this.$bottomDetails.show();

            }

            var self = this;

            // remove the current image in the preview
            if (typeof self.$largeImg != 'undefined') {
                self.$largeImg.remove();
            }

            // preload large image and add it to the preview
            if (self.$fullimage.is(':visible')) {
                this.$loading.show();
                $('<img/>').load(function() {
                    var $img = $(this);
                    if ($img.attr('src') === self.$item.children('a').data('largesrc')) {
                        self.$loading.hide();
                        self.$fullimage.find('img').remove();
                        self.$largeImg = $img.fadeIn(350);
                        self.$fullimage.append(self.$largeImg, self.$fullimageCredit);
                    }
                }).attr('src', eldata.largesrc);
            }

        },
        open: function() {

            setTimeout($.proxy(function() {
                // set the height for the preview and the item
                this.setHeights();
                // scroll to position the preview in the right place
                this.positionPreview();
            }, this), 25);

        },
        close: function() {

            var self = this,
                onEndFn = function() {
                    if (support) {
                        $(this).off(transEndEventName);
                    }
                    self.$item.removeClass('og-expanded');
                    self.$previewEl.remove();
                };

            setTimeout($.proxy(function() {

                if (typeof this.$largeImg !== 'undefined') {
                    this.$largeImg.fadeOut('fast');
                }
                this.$previewEl.css('height', 0);
                // the current expanded item (might be different from this.$item)
                var $expandedItem = $items.eq(this.expandedIdx);
                $expandedItem.css('height', '').on(transEndEventName, onEndFn);

                if (!support) {
                    onEndFn.call();
                }

            }, this), 25);

            return false;

        },
        calcHeight: function() {
            if (window.matchMedia('(max-width: 767px)').matches) {
                var heightPreview = this.$fullimage.height() + this.$details.outerHeight(true) + this.$bottomDetails.outerHeight(true) + 60,
                    itemHeight = heightPreview + this.$item.data('height') + marginExpanded;
            } else {
                var heightPreview = winsize.height - this.$item.data('height') - marginExpanded,
                    itemHeight = winsize.height;

                if (heightPreview < settings.minHeight) {
                    heightPreview = settings.minHeight;
                    itemHeight = settings.minHeight + this.$item.data('height') + marginExpanded;
                }
            }

            this.height = heightPreview;
            this.itemHeight = itemHeight;

        },
        setHeights: function() {

            var self = this,
                onEndFn = function() {
                    if (support) {
                        self.$item.off(transEndEventName);
                    }
                    self.$item.addClass('og-expanded');
                };

            this.calcHeight();
            this.$previewEl.css('height', this.height);
            this.$item.css('height', this.itemHeight).on(transEndEventName, onEndFn);

            if (!support) {
                onEndFn.call();
            }

        },
        positionPreview: function() {

            // scroll page
            // case 1 : preview height + item height fits in window´s height
            // case 2 : preview height + item height does not fit in window´s height and preview height is smaller than window´s height
            // case 3 : preview height + item height does not fit in window´s height and preview height is bigger than window´s height
            var position = this.$item.data('offsetTop'),
                previewOffsetT = this.$previewEl.offset().top - scrollExtra,
                scrollVal;

                if (this.height + this.$item.data('height') + marginExpanded <= winsize.height) {
                    scrollVal = position;
                }
                else if (this.height < winsize.height) {
                    scrollVal = previewOffsetT - (winsize.height - this.height);
                }
                else {
                    scrollVal = previewOffsetT;
                }

            $body.animate({
                scrollTop: scrollVal
            }, settings.speed);
        },
        setTransition: function() {
            this.$previewEl.css('transition', 'height ' + settings.speed + 'ms ' + settings.easing);
            this.$item.css('transition', 'height ' + settings.speed + 'ms ' + settings.easing);

        },
        getEl: function() {
            return this.$previewEl;
        }
    }

    return {
        init: init,
        addItems: addItems
    };
})();
