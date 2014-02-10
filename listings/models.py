from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    about_me = models.TextField(null=True, blank=True)
    # TODO : add fields to profile
    # TODO: list offers/requests of any user
    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    # class Meta:
    #     db_table = 'user_profile'

    def profile_image_url(self):
        """
        Return the URL for the user's Facebook icon if the user is logged in via Facebook,
        otherwise return the user's Gravatar URL
        """
        # TODO: add picture from google
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(
            hashlib.md5(self.user.email).hexdigest())

    def account_verified(self):
        """
        If the user is logged in and has verified hisser email address, return True,
        otherwise return False
        """
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name

    def count_offers(self):
        return Listing.objects.filter(listing_type = Listing.OFFER, tags = self).count()

    def count_requests(self):
        return Listing.objects.filter(listing_type = Listing.REQUEST, tags = self).count()

class Listing(models.Model):
    # DONETODO : add CRUD (Create / Read / Update / Delete) views:
    #   we did post new listing and view listing
    #   DONETODO: delete button in the view (if owner of the listing)
    #   DONETODO: edit button in the view (if owner of the listing)
    #   DONETODO: edit form of the listing + delete button
    #   DONETODO: delete icon in "my listings" list for each item
    #   TODO: if not owner of offer, button "request this item",
    #         if not owner of request, button "offer this item"
    #         + form of send message + send via email + link from email + inbox etc
    # TODO: map view with offers/requests on map

    OFFER = 1
    REQUEST = 2
    LISTING_TYPES = (
        (OFFER, "Offer"),
        (REQUEST, "Request"),
    )
    LISTING_SLUGS = {
        OFFER: 'offers',
        REQUEST: 'requests',
    }

    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    listing_type = models.IntegerField(choices=LISTING_TYPES, default=OFFER)


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


class ContactMessage(models.Model):

    msg_sender = models.ForeignKey(User, related_name="sent_messages")
    msg_receiver = models.ForeignKey(User, related_name="received_messages")
    listing = models.ForeignKey(Listing)
    created_at = models.DateTimeField(auto_now_add=True)
    msg_title = models.CharField(max_length=200)
    msg_body = models.TextField()
