Gear Tracker
============

Gear Tracker is an inventory system for wilderness travel and backpacking gear. It runs on [Django](http://www.djangoproject.com/).


Genesis
--------

Weight is an important consideration when travelling in wilderness places. A digital scale is a useful tool to measure the weight of individual items. If you know the weight of an item, you can more accurately judge whether the item should be added to your pack.

When I first bought my scale, I started a spreadsheet containing the weights of various pieces of gear. It seemed like a good idea -- I knew I wanted some sort of database to store my measured weights and other notes in -- but I never got around to updating it. Data in a spreadsheet is too static. You can't do much with it. I think that characteristic contributed to my disinterest with the spreadsheet. So, I decided to write an application to fill my needs.

Features
--------


### Metric and Imperial Weights

Weights are always input in grams, but can be displayed in either metric (grams, kilograms) or imperial (ounces, pounds) units.


### Public/Private Gear Lists

A gear list can be marked either public or private.

If a gear list is private, it will only be viewable to logged in users who have permissions to create a gear list. The intent behind allowing private lists is that you can create your gear list before you leave on a trip, but not make the gear list public until after you have returned. Thus, your trip is not public knowledge until you make it back.


### Archivable Items

Items can be archived.

When an item is archived, it will not be displayed in any list of items (such as the All Gear list, or list of items by category/type/tag). The item's page will continue to exist, so that any hard-coded links (from your site or others) will not be broken.

Archived items will continue to appear in any gear lists they might belong to. This is to retain the historical accuracy of the gear lists, and to avoid screwing with weights. The archived item's name will not be a link to the item's page, and the table row of the archived item will have a unique class applied to it so that the user may style it differently than non-archived items.

The idea behind archivable items is that if you no longer possess an item, you may not want it to appear in your list of items. But you may want to retain the item's entry so that you can reference its weight in the future, and you don't want to delete the item outright for fear of thus invalidating old gear lists which that item may appear in.


Installation
------------

1.  Put the `geartracker` directory somewhere in your Python path (like inside your Django project folder).

2.  Add `geartracker` to your `settings.INSTALLED_APPS`.


Requirements
------------

* [sorl-thumbnail](http://thumbnail.sorl.net/) is used to generate thumbnails of images.
* [Python Imaging Library](http://www.pythonware.com/products/pil/) is required for getting photo EXIF data.
* [django-taggit](https://github.com/alex/django-taggit) is required for tagging.
* [django-taggit-templatetags](https://github.com/feuervogel/django-taggit-templatetags) is required for listing tags in templates.


Feedback
--------

If you use Gear Tracker, I'd be interested to hear any feedback you might have. [Contact me via email](mailto:pm@pig-monkey.com).

From the user perspective, I'm keen to hear whether the app fills your needs or not.

I am new to both Django and Python, so, from the developer perspective, I would appreciate any feedback on the code.
