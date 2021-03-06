from django.conf.urls import *
from django.views.generic import TemplateView

from geartracker.views import *

urlpatterns = patterns('',
    url(r'^$',
        view = index,
        name = 'geartracker'
    ),
    url(r'^all/$',
        view=ItemListView.as_view(),
        name='geartracker_item_list'
    ),
    url(r'^category/$',
        view=CategoryListView.as_view(),
        name='geartracker_category_list'
    ),
    url(r'^category/(?P<slug>[-\w]+)/$',
        view=CategoryDetailView.as_view(),
        name='geartracker_category_detail'
    ),
    url(r'^category/(?P<category>[-\w]+)/(?P<slug>[-\w]+)/$',
        view=TypeDetailView.as_view(),
        name = 'geartracker_type_detail'
    ),
    url(r'^tags/$',
        view=TemplateView.as_view(template_name='geartracker/tag_list.html'),
        name='geartracker_tag_list'
    ),
    url(r'^tags/(?P<slug>[-\w]+)/$',
        view=TagDetailView.as_view(),
        name='geartracker_tag_detail'
    ),
    url(r'^list/$',
        view=ListListView.as_view(),
        name='geartracker_list_list'
    ),
    url(r'^list/(?P<slug>[-\w]+)/$',
        view=ListDetailView.as_view(),
        name='geartracker_list_detail'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        view=ItemDetailView.as_view(),
        name='geartracker_item_detail'
    ),
)
