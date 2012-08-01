from operator import attrgetter, itemgetter

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import list_detail
from django.http import Http404
from django.views.generic import DetailView, ListView

from taggit.models import Tag

from geartracker.models import *


class ItemDetailView(DetailView):
    """Display a single item."""
    model = Item


class ItemListView(ListView):
    """Display a list of items."""
    model = Item


class CategoryListView(ListView):
    """Display a list of categories."""
    model = Category


class CategoryDetailView(DetailView):
    """Display all items in a given category."""
    model = Category

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        # Add in a queryset of all items in the category.
        context['object_list'] = Item.objects.all().filter(category__slug=self.kwargs['slug'])
        return context


class TypeDetailView(DetailView):
    """Display all items of a given type."""
    model = Type

    def get_object(self):
        # Get the requested type. Raise a 404 if it does not exist.
        object = get_object_or_404(Type,
                                   category__slug=self.kwargs['category'],
                                   slug=self.kwargs['type'])
        return object

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(TypeDetailView, self).get_context_data(**kwargs)
        # Add in a queryset of all items of the type.
        context['object_list'] = Item.objects.all().filter(type__slug=self.kwargs['type'])
        return context

class TagDetailView(DetailView):
    """Display all items with a given tag."""
    model = Tag
    template_name = 'geartracker/items_by_tag.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(TagDetailView, self).get_context_data(**kwargs)
        # Add in a queryset of all items with the given tag.
        context['object_list'] = Item.objects.all().filter(tags__slug=self.kwargs['slug'])
        return context


def index(request):

    # Get items
    items = Item.objects.filter(archived=False).order_by('-acquired')

    # Get lists
    lists = List.objects.filter(public=True)

    return render_to_response('geartracker/index.html',
                              {'item_list': items[:6],
                               'list_list': lists[:6]},
                              context_instance=RequestContext(request))


def gearlist_detail(request, slug):

    # Look up item (and raise a 404 if it can't be found).
    list = get_object_or_404(List, slug=slug)

    # A list is only viewable if the user is authenticated or if the list is
    # public. geartracker.add_list
    if request.user.has_perm('geartracker.add_list') or list.public:
        # Get all packed items and sort them by category, then type.
        packed_items = ListItem.objects.filter(list=list, type='packed')
        packed_items = sorted(packed_items,
                              key=attrgetter('item.category.name',
                                             'item.type.name'),
                              reverse=False)

        # Get all worn items and sort them by category, then type.
        worn_items = ListItem.objects.filter(list=list, type='worn')
        worn_items = sorted(worn_items,
                            key=attrgetter('item.category.name',
                                           'item.type.name'),
                            reverse=False)

        return list_detail.object_detail(
            request,
            queryset=List.objects.all(),
            object_id=list.id,
            template_name='geartracker/list_detail.html',
            template_object_name='list',
            extra_context={'packed_items': packed_items,
                           'worn_items': worn_items}
        )
    # Anonymous users get a 404 when they try to view non-public lists
    else:
        raise Http404
