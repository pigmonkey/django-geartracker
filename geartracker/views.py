from operator import attrgetter, itemgetter

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import DetailView, ListView, TemplateView

from taggit.models import Tag

from geartracker.models import *
from geartracker import settings


class ItemDetailView(DetailView):
    """Display a single item."""
    queryset = Item.objects.published()


class ItemListView(ListView):
    """Display a list of items."""
    queryset = Item.objects.published()
    paginate_by = settings.GEARTRACKER_PAGINATE_BY


class CategoryListView(ListView):
    """Display a list of categories."""
    model = Category


class CategoryDetailView(ListView):
    """Display all items in a given category."""
    paginate_by = settings.GEARTRACKER_PAGINATE_BY

    def category(self, **kwargs):
        return get_object_or_404(Category, slug=self.kwargs['slug'])

    def get_queryset(self, **kwargs):
        return Item.objects.published().filter(category=self.category)

    def get_template_names(self, **kwargs):
        return 'geartracker/category_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        # Add the category to the context.
        context['category'] = self.category
        return context


class TypeDetailView(ListView):
    """Display all items of a given type."""
    paginate_by = settings.GEARTRACKER_PAGINATE_BY

    def category(self, **kwargs):
        return get_object_or_404(Category, slug=self.kwargs['category'])

    def type(self, **kwargs):
        return get_object_or_404(Type, category=self.category,
                                 slug=self.kwargs['slug'])

    def get_queryset(self, **kwargs):
        return Item.objects.published().filter(type=self.type)

    def get_template_names(self, **kwargs):
        return 'geartracker/type_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(TypeDetailView, self).get_context_data(**kwargs)
        # Add the category to the context.
        context['category'] = self.category
        # Add the type to the context.
        context['type'] = self.type
        return context

class TagDetailView(ListView):
    """Display all items with a given tag."""
    def tag(self, **kwargs):
        return get_object_or_404(Tag, slug=self.kwargs['slug'])

    def get_queryset(self, **kwargs):
        return Item.objects.published().filter(tags=self.tag)

    def get_template_names(self, **kwargs):
        return 'geartracker/tag_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context.
        context = super(TagDetailView, self).get_context_data(**kwargs)
        # Add in the tag to the context.
        context['tag'] = self.tag
        return context


class ListListView(ListView):
    """Display a list of gear lists."""
    paginate_by = settings.GEARTRACKER_PAGINATE_BY

    def get_queryset(self, **kwargs):
        return List.objects.filter(public=True)


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
        if (not object.public and not
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
    items = Item.objects.published().order_by('-acquired')

    # Get lists
    lists = List.objects.public()

    return render_to_response('geartracker/index.html',
                              {'item_list': items[:6],
                               'list_list': lists[:6]},
                              context_instance=RequestContext(request))
