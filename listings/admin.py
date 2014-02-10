from listings import models
from django.contrib import admin


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class ListingAdmin(admin.ModelAdmin):
    list_display = (
                    "title",
                    "organization_name",
                    "created_at",
                    "geographic_area",
                    "tag_list",
                    )


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
                    "msg_sender",
                    "msg_receiver",
                    "listing",
                    "created_at",
                    "msg_title",
                    "msg_body",
                    )



admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Listing, ListingAdmin)
admin.site.register(models.ContactMessage, ContactMessageAdmin)