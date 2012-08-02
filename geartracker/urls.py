from django.conf.urls.defaults import *

from geartracker.models import *
from geartracker.views import *

urlpatterns = patterns('',
    url(r'^$',
        view = index,
        name = 'geartracker_home'
    ),
    url(r'^category/(?P<category>[-\w]+)/(?P<type>[-\w]+)/$',
        view=TypeItemsView.as_view(),
        name = 'geartracker_type_items'
    ),
    url(r'^category/(?P<slug>[-\w]+)/$',
        view=CategoryItemsView.as_view(),
        name='geartracker_category_items'
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
        view=TagListView.as_view(),
        name='geartracker_tag_list'
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
