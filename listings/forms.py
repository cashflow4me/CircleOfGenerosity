import floppyforms as forms
from listings.models import Listing, ContactMessage

# This is for both create and edit listing
class CreateListingForm(forms.ModelForm):

    # source =

    class Meta:
        model = Listing
        exclude = [
            'owner'
        ]
        # fields = (
        #            'title',
        #            'abstract',
        #            )

        widgets = {
            'company_name': forms.TextInput,
            'company_url': forms.URLInput,
            'title': forms.TextInput,
            'description': forms.Textarea,
            'apply_email': forms.EmailInput,
            'geographic_area': forms.TextInput,
            'tags': forms.SelectMultiple
        }


class CreateContactMessageForm(forms.ModelForm):

    # source =

    class Meta:
        model = ContactMessage
        # item = Listing
        # listing_title = item.organization_name

        exclude = [
                  # 'msg_sender',
                  'msg_receiver',
                  'listing',
                  ]
        # fields = (
        #           'msg_title',
        #           'msg_body',
        #            )

        widgets = {
            'msg_sender': forms.TextInput({"value": '2'}),
            'msg_title': forms.TextInput({"value": "alex"}),
            'msg_body': forms.Textarea,
        }

    def get_context_data(self):
        ctx = super(CreateContactMessageForm, self).get_context_data()
        ctx['msg_sender'] = 'bar'
        return ctx

