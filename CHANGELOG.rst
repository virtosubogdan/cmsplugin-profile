CHANGELOG
=========

Revision 0293589 (25.11.2015, 11:00 UTC)
----------------------------------------

* LUN-2808

  * scrolling and resize on mobile/tablet fix

* LUN-2814

  * Also save the selection for the link target so it can be restored.
  * Fix values for profile link target selection.

* LUN-2816

  * added off() also on delegated function
  * multiple click triggers on link fixed with off()

* LUN-2817

  * Escape only html.

* LUN-2818

  * Fix: Input value with total form count was not increased correctly.

No other commits.

Revision 94d7f47 (23.11.2015, 10:31 UTC)
----------------------------------------

* LUN-2698

  * global variable transformed to local by mistake fixed
  * renamed js files that are dependent of jquery
  * missed comma  added
  * update after code review
  * namespaced the plugin so that we can have many grids/promos on a page
  * word-wraping added on other elements as well
  * convert tabs to spaces
  * Firefox bug fixed with max-width on image
  * prettify file
  * fix bug due to html entities
  * bug fixed with no-wrapping title

* LUN-2744

  * Fix bug: Profile selection was not maintained if validation failed.
  * New selected profiles were always added but never removed.
  * Move new_profile request in the admin url namespace.
  * Remove authentication check for front end "load more profiles" request.

* LUN-2807

  * Profile plugin issues fixed on dark theme

* LUN-2808

  * profile preview closes at window resize - fixed

* Misc commits

  * correct path to jquery resources for the grid

Revision 04a649e (17.11.2015, 13:36 UTC)
----------------------------------------

Changelog history starts here.
