from listings.models import Listing
from django.shortcuts import render
from django.views.generic.edit import CreateView


def home(request):
    qs = Listing.objects.order_by('-created_at')
    return render(request, 'listings/ad_list.html', {
                            'object_list': qs})


def listing(request, pk):
    listing = Listing.objects.get(id=int(pk))
    return render(request, 'listings/ad_detail.html', {
                            'object': listing})


class PostListingView(CreateView):
    model = Listing