from listings.models import Tag, Listing
from django.test import TestCase


class ListingsTest(TestCase):

    def test_create_listings(self):

        tag1 = Tag.objects.create(name="Tangible", slug="tangible")
        tag2 = Tag.objects.create(name="Skill/Service", slug="skill_service")
        tag3 = Tag.objects.create(name="Transport", slug="transport")
        tag4 = Tag.objects.create(name="Space", slug="space")

        self.assertEquals(0, Listing.objects.count())

        listing1 = Listing()
        listing1.company_name = "ACME International"
        listing1.company_url = "http://acme.com/"
        listing1.title = "Ninja Top Developer"
        listing1.description = """
We are growing, we need more developers.
Apply if you are cool and sexy.
"""
        listing1.apply_email = "jobs@acme.com"

        listing1.full_clean()
        listing1.save()

        # self.assertEquals(1, Listing.objects.count())
        #
        # listing1.tags.add(tag1)
        #
        # self.assertEquals(1, tag1.listings.count())
        #
        # tag2.listings.add(listing1)
        #
        # self.assertEquals(2, listing1.tags.count())
        #
        # self.assertEquals(0, tag3.listings.count())
        #
        # self.assertEquals(0, tag4.listings.count())
        #
        # tag4.listings.add(listing1)
        #
        # self.assertEquals(1, tag4.listings.count())