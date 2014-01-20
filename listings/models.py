from django.core.urlresolvers import reverse
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class Listing(models.Model):
    OFFER = 1
    REQUEST = 2

    created_at = models.DateTimeField(auto_now_add=True)

    listing_type = models.IntegerField(choices=(
        (OFFER, "Offer"),
        (REQUEST, "Request"),
    ), default=OFFER)

    organization_name = models.CharField(max_length=200)
    organization_url = models.URLField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    apply_email = models.EmailField()
    geographic_area = models.CharField(max_length=200, null=True,
                                       blank=True)

    tags = models.ManyToManyField(Tag, related_name="listings", blank=True)

    def __unicode__(self):
        return self.title

    def tag_list(self):
        return ", ".join([tag.name for tag in self.tags.all()])
    tag_list.short_description = "Tags"

    def get_absolute_url(self):
        return reverse('listing', args=(self.id,))
