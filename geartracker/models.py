from django.db import models
from geartracker.mass import metric, imperial
from sorl.thumbnail import ImageField

class Category(models.Model):
    """ Model representing a category """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ('name',)
    
    @property
    def number_items(self):
        return len(self.item_set.all())

    def __unicode__(self):
        return self.name

class Type(models.Model):
    """ Model representing a type """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category)

    class Meta:
        ordering = ('category', 'name',)
    
    @property
    def number_items(self):
        return len(self.item_set.all())
    
    @property
    def separator(self):
        return '::'
    
    def __unicode__(self):
        #return self.name
        return u'%s %s %s' % (self.category, self.separator, self.name)

class Tag(models.Model):
    """ Model representing a tag """
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('slug',)
    
    @property
    def number_items(self):
        return len(self.item_set.all())

    def __unicode__(self):
        return self.slug

class Item(models.Model):
    """ Model representing an item """
    make = models.CharField(max_length=100,
        help_text="Required. The make (or brand) of the item.")
    model = models.CharField(max_length=100,
        help_text="Required. The model of the item.")
    slug = models.SlugField(unique=True,
        help_text="Required. The slug is used to build the item's URL.")
    weight = models.PositiveIntegerField(verbose_name="Weight (grams)",
        help_text="Required. Weight in grams only. Do not include units.")
    acquired = models.DateField(
        help_text="Required. The date on which this item was acquired.")
    type = models.ForeignKey(Type,
        help_text="Required. The item's type specifies how it is organized.")
    size = models.CharField(max_length=30, blank=True,
        help_text="An optional size for the item.")
    link = models.URLField(blank=True, null=True,
        help_text="An optional link to the manufacturer's page for the item.")
    review_url = models.URLField(blank=True, null=True,
        help_text="An optional link to a review of the item.")
    notes = models.TextField(blank=True,
        help_text="Any optional notes on the item.")
    image = models.ImageField(upload_to='geartracker/images/gear/', blank=True,
        help_text="An optional image of the item.")
    category = models.ForeignKey(Category, editable=False)
    tags = models.ManyToManyField(Tag, blank=True,
        help_text="Any optional tags for the item.")
    related = models.ManyToManyField("self", blank=True,
        help_text="Any items that are related to this item. Optional.")
    archived = models.BooleanField(default=False,
        help_text="Archive this item.")
    
    class Meta:
        ordering = ('make', 'model')
    
    def __unicode__(self):
        if self.size:
            return u'%s %s (%s)' % (self.make, self.model, self.size)
        else:
            return u'%s %s' % (self.make, self.model)

    @property
    def name(self):
        return self.__unicode__()

    @property
    def metric_weight(self):
        return metric(self.weight)

    @property
    def imperial_weight(self):
        return imperial(self.weight)

    def save(self, *args, **kwargs):
        # Set the item's category to whatever the type's category is.
        self.category = self.type.category
        # Call the real save.
        super(Item, self).save(*args, **kwargs)

class ListItem(models.Model):
    """ Model representing an item in a gear list """
    CARRY_CHOICES = (
        ('packed', 'Packed'),
        ('worn', 'Worn'),
    )
    item = models.ForeignKey(Item)
    list = models.ForeignKey('List')
    quantity = models.PositiveIntegerField(default=1)
    type = models.CharField(max_length=6, choices=CARRY_CHOICES)
    
    def __unicode__(self):
        return u'%s (%sx)' % (self.item, self.quantity)

    @property
    def total_weight(self):
        return self.quantity * self.item.weight

    @property
    def total_metric_weight(self):
        return metric(self.quantity * self.item.weight)
    
    @property
    def total_imperial_weight(self):
        return imperial(self.quantity * self.item.weight)

class List(models.Model):
    """ Model representing a gear list """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    trip_report = models.URLField(blank=True, null=True, help_text="An option URL to a trip report.")
    public = models.BooleanField(default=True, help_text="Should this list be publicly viewable?")
    items = models.ManyToManyField(Item, through=ListItem)

    class Meta:
        ordering = ('-start_date', 'end_date')
    
    def __unicode__(self):
        return self.name

    def clean(self):
        from django.core.exceptions import ValidationError
        # Trip end date must be greater than start date
        if self.end_date < self.start_date:
            raise ValidationError('End date must be greater than or equal to start date.')

    def add_weight(self, items):
        total_weight = 0
        for item in items:
            total_weight += item.total_weight
        return total_weight

    @property
    def packed_weight(self):
        list_items = ListItem.objects.filter(list=self, type='packed')
        return self.add_weight(list_items)

    @property
    def packed_metric_weight(self):
        return metric(self.packed_weight)

    @property
    def packed_imperial_weight(self):
        return imperial(self.packed_weight)

    @property
    def worn_weight(self):
        list_items = ListItem.objects.filter(list=self, type='worn')
        return self.add_weight(list_items)

    @property
    def worn_metric_weight(self):
        return metric(self.worn_weight)

    @property
    def worn_imperial_weight(self):
        return imperial(self.worn_weight)

    @property
    def total_weight(self):
        list_items = ListItem.objects.filter(list=self)
        return self.add_weight(list_items)

    @property
    def total_metric_weight(self):
        return metric(self.total_weight)

    @property
    def total_imperial_weight(self):
        return imperial(self.total_weight)
