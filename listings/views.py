from listings.forms import CreateListingForm
from listings.models import Listing
from django.shortcuts import render
from django.views.generic.edit import CreateView


def home(request):
    qs = Listing.objects.order_by('-created_at')
    return render(request, 'listings/listing_list.html', {
                            'object_list': qs})


def listing(request, pk):
    listing = Listing.objects.get(id=int(pk))
    return render(request, 'listings/listing_details.html', {
                            'object': listing})



class PostListingView(CreateView):
    model = Listing
    form_class = CreateListingForm