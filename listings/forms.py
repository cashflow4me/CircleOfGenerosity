import floppyforms as forms
from listings.models import Listing


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
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


