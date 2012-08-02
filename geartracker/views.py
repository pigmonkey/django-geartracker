from operator import attrgetter, itemgetter

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import DetailView, ListView, TemplateView

from taggit.models import Tag

from geartracker.models import *
from geartracker import settings


class ItemDetailView(DetailView):
    """Display a single item."""
    model = Item


class ItemListView(ListView):
    """Display a list of items."""
    model = Item
    paginate_by = settings.GEARTRACKER_PAGINATE_BY


class CategoryListView(ListView):
    """Display a list of categories."""
    model = Category


class CategoryItemsView(ListView):
    """Display all items in a given category."""
    paginate_by = settings.GEARTRACKER_PAGINATE_BY

    def category(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return category

    def get_queryset(self):
        # Get the requested items.
        queryset = Item.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(CategoryItemsView, self).get_context_data(**kwargs)
        # Add the category object to the context.
        context['category'] = self.category
        # Set the page title to the category name.
        context['title'] = self.category
        return context


class TypeItemsView(ListView):
    """Display all items of a given type."""
    paginate_by = settings.GEARTRACKER_PAGINATE_BY

    def category(self):
        category = Category.objects.get(slug=self.kwargs['category'])
        return category

    def type(self):
        type = Type.objects.get(category=self.category,
                                slug=self.kwargs['type'])
        return type

    def get_queryset(self):
        # Get the requested items.
        queryset = Item.objects.filter(type=self.type)
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(TypeItemsView, self).get_context_data(**kwargs)
        # Add the category object to the context.
        context['category'] = self.category
        # Add the type object to the context.
        context['type'] = self.type
        # Set the page title to the type name.
        context['title'] = self.type
        return context


class TagListView(TemplateView):
    """Display a list of tags."""
    template_name = 'geartracker/tag_list.html'


class TagItemsView(ListView):
    """Display all items with a given tag."""
    paginate_by = settings.GEARTRACKER_PAGINATE_BY

    def tag(self):
        tag = Tag.objects.get(slug=self.kwargs['slug'])
        return tag

    def get_queryset(self):
        # Get the requested items.
        queryset = Item.objects.filter(tags=self.tag)
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(TagItemsView, self).get_context_data(**kwargs)
        # Add the tag object to the context.
        context['tag'] = self.tag
        # Set the page title to the tag name.
        context['title'] = self.tag
        return context


class ListListView(ListView):
    """Display a list of gear lists."""
    model = List
    paginate_by = settings.GEARTRACKER_PAGINATE_BY


class ListDetailView(DetailView):
    """Display a single gear list."""
    model = List

    def get_object(self):
        object = List.objects.get(slug=self.kwargs['slug'])
        # Only return the list if it is public or the user has the proper
        # permissions.
        if self.request.user.has_perm('geartracker.add_list') or object.public:
            return object
        else:
            return None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(ListDetailView, self).get_context_data(**kwargs)
        # Get all packed items and sort them by category, then type.
        packed_items = ListItem.objects.filter(list=self.get_object(),
                                               type='packed')
        packed_items = sorted(packed_items,
                              key=attrgetter('item.category.name',
                                             'item.type.name'),
                              reverse=False)
        # Add the packed items to the context.
        context['packed_items'] = packed_items

        # Get all worn items and sort them by category, then type.
        worn_items = ListItem.objects.filter(list=self.get_object(),
                                             type='worn')
        worn_items = sorted(worn_items,
                            key=attrgetter('item.category.name',
                                           'item.type.name'),
                            reverse=False)
        # Add the worn items to the context.
        context['worn_items'] = worn_items
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
