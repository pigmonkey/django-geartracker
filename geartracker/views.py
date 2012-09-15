from operator import attrgetter, itemgetter

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
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


class CategoryDetailView(DetailView):
    """Display all items in a given category."""
    model = Category
    paginate_by = settings.GEARTRACKER_PAGINATE_BY

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        # Add a queryset of all items in the category.
        context['object_list'] = Item.objects.filter(category__slug=self.kwargs['slug'])
        return context


class TypeDetailView(DetailView):
    """Display all items of a given type."""
    paginate_by = settings.GEARTRACKER_PAGINATE_BY

    def category(self):
        try:
            category = Category.objects.get(slug=self.kwargs['category'])
        except ObjectDoesNotExist:
            raise Http404
        return category

    def get_object(self):
        try:
            type = Type.objects.get(category=self.category,
                                    slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            raise Http404
        return type

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(TypeDetailView, self).get_context_data(**kwargs)
        # Add the category object to the context.
        context['category'] = self.category
        # Add a queryset of all items of the type.
        context['object_list'] = Item.objects.filter(type=self.get_object())
        return context

class TagDetailView(DetailView):
    """Display all items with a given tag."""
    model = Tag
    template_name = 'geartracker/tag_detail.html'
    paginate_by = settings.GEARTRACKER_PAGINATE_BY

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(TagDetailView, self).get_context_data(**kwargs)
        # Add in a queryset of all items with the given tag.
        context['object_list'] = Item.objects.filter(tags__slug=self.kwargs['slug'])
        return context


class ListListView(ListView):
    """Display a list of gear lists."""
    model = List
    paginate_by = settings.GEARTRACKER_PAGINATE_BY


class ListDetailView(DetailView):
    """Display a single gear list."""
    model = List

    def get_object(self):
        try:
            object = List.objects.get(slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            raise Http404
        # Raise a 404 if the list is not public and the user does not have
        # permissions.
        if (not object.public and
                self.request.user.has_perm('geartracker.add_list')):
            raise Http404

        return object

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
