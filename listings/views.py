from listings.forms import CreateListingForm
from listings.models import Listing, Tag
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView


def home(request):
    # qs = Listing.objects.order_by('-created_at')
    tagList = Tag.objects.all()
    return render(request, 'home_page.html', {
                            'object_list': tagList})
                            # 'object_list': qs})


def listing(request, pk):
    listing = Listing.objects.get(id=int(pk))
    return render(request, 'listings/listing_details.html', {
                            'object': listing})


def listings_by_type(request,type):
    theList = Listing.objects.filter(listing_type=type)
    tagList = Tag.objects.all()
    return render(request, 'listings/listing_list.html', {
                            'object_list': theList,
                            'tag_list': tagList})


def listings_by_tag_slug(request, pk, type):
    tag=get_object_or_404(Tag, slug=pk)
    theList = Listing.objects.filter(listing_type=type, tags=tag)
    return render(request, 'listings/listing_list.html', {
                            'object_list': theList})

def listings_by_tag_id(request, pk, type):
    tag=get_object_or_404(Tag, pk=pk)
    theList = Listing.objects.filter(listing_type=type, tags=tag)
    return render(request, 'listings/listing_list.html', {
                            'object_list': theList})


class PostListingView(CreateView):
    model = Listing
    form_class = CreateListingForm