from operator import attrgetter, itemgetter

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import list_detail
from django.http import Http404
from django.views.generic import DetailView

from taggit.models import Tag

from geartracker.models import *


def item_detail(request, slug):

    # Look up item (and raise a 404 if it can't be found).
    item = get_object_or_404(Item, slug=slug)

    return list_detail.object_detail(
        request,
        queryset=Item.objects.all(),
        object_id=item.id,
        template_name='geartracker/item_detail.html',
        template_object_name='item',
    )


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


def items_by_category(request, slug, page=1):

    # Look up type (and raise a 404 if it can't be found).
    category = get_object_or_404(Category, slug=slug)

    # Use the generic object_list view to return the list of items
    return list_detail.object_list(
        request,
        queryset=Item.objects.filter(category=category, archived=False),
        template_name='geartracker/items_by_category.html',
        template_object_name='item',
        extra_context={'category': category},
        paginate_by=12,
        page=page
    )


def items_by_type(request, cat_slug, type_slug, page=1):

    # Look up type (and raise a 404 if it can't be found).
    type = get_object_or_404(Type, slug=type_slug)

    # Look up category (and raise a 404 if it can't be found).
    category = get_object_or_404(Category, slug=cat_slug)

    # Use the generic object_list view to return the list of items
    return list_detail.object_list(
        request,
        queryset=Item.objects.filter(type=type, archived=False),
        template_name='geartracker/items_by_type.html',
        template_object_name='item',
        extra_context={'type': type, 'category': category},
        paginate_by=12,
        page=page
    )

class TagDetailView(DetailView):
    """Display all items with a given tag."""
    model = Tag
    template_name = 'geartracker/items_by_tag.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(TagDetailView, self).get_context_data(**kwargs)
        # Add in a queryset of all items with the given tag.
        context['object_list'] = Item.objects.published().filter(tags__slug=self.kwargs['slug'])
        return context


def categories_view(request, match):

    # Get all categories.
    categories = Category.objects.all()

    # For each category, get all related types
    category_list = []
    for category in categories:
        category_list.append({'category': category,
                             'types': Type.objects.filter(category=category)})

    # Return the dictionary of categories and types to the template
    return render_to_response('geartracker/category_list.html',
                              {'categories': category_list},
                              context_instance=RequestContext(request))


def index(request):

    # Get items
    items = Item.objects.filter(archived=False).order_by('-acquired')

    # Get lists
    lists = List.objects.filter(public=True)

    return render_to_response('geartracker/index.html',
                              {'item_list': items[:6],
                               'list_list': lists[:6]},
                              context_instance=RequestContext(request))
