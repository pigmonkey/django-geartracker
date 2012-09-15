from django.db.models import Manager


class PublicListManager(Manager):

    def public(self):
        """Return public lists."""
        return self.get_query_set().filter(public=True)


class ArchivedItemManager(Manager):

    def published(self):
        """Return items that are not archived."""
        return self.get_query_set().filter(archived=False)
