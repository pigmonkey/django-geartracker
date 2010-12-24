from django.conf.urls.defaults import *
from django.views.generic import list_detail
from geartracker.models import Item, Category, Type, Tag, List
from geartracker.views import index, items_by_category, items_by_type, items_by_tag, item_detail, gearlist_detail, categories_view

items = {
    'queryset': Item.objects.filter(archived=False),
    'template_object_name': 'item',
    'template_name': 'geartracker/all_items.html',
    'paginate_by': 12
}

tags = {
    'queryset': Tag.objects.all(),
    'template_object_name': 'tag',
}

lists = {
    'queryset': List.objects.filter(public=True),
    'template_object_name': 'list',
    'paginate_by': 12
}

urlpatterns = patterns('',
    (r'^$', index),
    (r'^all/$', list_detail.object_list, items, "items_view"),
    (r'^all/page/(?P<page>[0-9]+)/$',
        list_detail.object_list,
        items,
        "items_paginated"),
    (r'^categor(y|ies)/$', categories_view),
    (r'^category/(?P<slug>[-\w]+)/$', items_by_category),
    (r'^category/(?P<slug>[-\w]+)/page/(?P<page>[0-9]+)/$', items_by_category),
    (r'^category/(?P<cat_slug>[-\w]+)/(?P<type_slug>[-\w]+)/$', items_by_type),
    (r'^category/(?P<cat_slug>[-\w]+)/(?P<type_slug>[-\w]+)/page/(?P<page>[0-9]+)/$',
        items_by_type),
    (r'^tags?/$', list_detail.object_list, tags, "tags_view"),
    (r'^tags?/(?P<slug>[-\w]+)/$', items_by_tag),
    (r'^tags?/(?P<slug>[-\w]+)/page/(?P<page>[0-9]+)/$', items_by_tag),
    (r'^lists?/$', list_detail.object_list, lists, "lists_view"),
    (r'^lists?/page/(?P<page>[0-9]+)/$',
        list_detail.object_list,
        lists,
        "lists_paginated"),
    (r'^lists?/(?P<slug>[-\w]+)/$', gearlist_detail),
    (r'^(?P<slug>[-\w]+)/$', item_detail),
)
