from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from geartracker.models import *
from geartracker.views import *

lists = {
    'queryset': List.objects.filter(public=True),
    'template_object_name': 'list',
    'paginate_by': 12
}

urlpatterns = patterns('',
    url(r'^$',
        view = index,
        name = 'geartracker_home'
    ),
    url(r'^category/(?P<category>[-\w]+)/(?P<type>[-\w]+)/$',
        view=TypeDetailView.as_view(),
        name = 'geartracker_type_detail'
    ),
    url(r'^category/(?P<slug>[-\w]+)/$',
        view=CategoryDetailView.as_view(),
        name='geartracker_category_detail'
    ),
    url(r'^category/$',
        view=CategoryListView.as_view(),
        name='geartracker_category_list'
    ),
    url(r'^all/$',
        view=ItemListView.as_view(),
        name='geartracker_item_list'
    ),
    url(r'^tags/(?P<slug>[-\w]+)/$',
        view=TagDetailView.as_view(),
        name='geartracker_tag_detail'
    ),
    url(r'^tags/$',
        view=TemplateView.as_view(template_name='geartracker/tag_list.html'),
        name='geartracker_tag_list'
    ),
    (r'^lists?/$', list_detail.object_list, lists, "lists_view"),
    (r'^lists?/page/(?P<page>[0-9]+)/$',
        list_detail.object_list,
        lists,
        "lists_paginated"),
    (r'^lists?/(?P<slug>[-\w]+)/$', gearlist_detail),
    url(r'^(?P<slug>[-\w]+)/$',
        view=ItemDetailView.as_view(),
        name='geartracker_item_detail'
    ),
)
