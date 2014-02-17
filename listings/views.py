from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from listings.forms import CreateListingForm, CreateContactMessageForm
from listings.models import Listing, Tag, ContactMessage
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Count


def home(request):
    # qs = Listing.objects.order_by('-created_at')
    tagList = Tag.objects.all()
    my_offers = []
    my_requests = []
    # tags_with_counts = Tag.objects.all().annotate(listings_count=Count('listings__id'))
    if request.user.is_authenticated():
        # assert False, request.user
        my_offers = Listing.objects.filter(listing_type=Listing.OFFER, owner=request.user)
        # my_offers = Listing.objects.all()
        my_requests = Listing.objects.filter(listing_type=Listing.REQUEST, owner=request.user)

    return render(request, 'home_page.html', {
                            'object_list': tagList,
                            'my_offers': my_offers,
                            'my_requests': my_requests,
                            })
                            # 'object_list': qs})


def listing(request, pk):
    listing = Listing.objects.get(id=int(pk))
    return render(request, 'listings/listing_details.html', {
                            'object': listing})


class ListingOwnerMixin(object):

    model = Listing
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().owner:
            return HttpResponseForbidden("forbidden")
        return super(ListingOwnerMixin, self).dispatch(request, *args, **kwargs)


class EditListingView(ListingOwnerMixin, UpdateView):
    form_class = CreateListingForm


class DeleteListingView(ListingOwnerMixin, DeleteView):
    success_url = reverse_lazy('home')


def listings_by_type(request,type):
    theList = Listing.objects.filter(listing_type=type)
    tagList = Tag.objects.all()
    return render(request, 'listings/listing_list.html', {
                            'object_list': theList,
                            'tag_list': tagList,
                            'listing_type': Listing.LISTING_SLUGS[type]})


def listings_by_tag_slug(request, pk, type):
    tag=get_object_or_404(Tag, slug=pk)
    theList = Listing.objects.filter(listing_type=type, tags=tag)
    tagList = Tag.objects.all()
    return render(request, 'listings/listing_list.html', {
                            'object_list': theList,
                            'tag_list': tagList,
                            'listing_type': Listing.LISTING_SLUGS[type]})

def listings_by_tag_id(request, pk, type):
    tag=get_object_or_404(Tag, pk=pk)
    theList = Listing.objects.filter(listing_type=type, tags=tag)
    tagList = Tag.objects.all()
    return render(request, 'listings/listing_list.html', {
                            'object_list': theList,
                            'tag_list': tagList,
                            'listing_type': Listing.LISTING_SLUGS[type]})


class PostListingView(CreateView):
    model = Listing
    form_class = CreateListingForm

    def form_valid(self, form):
        #assert False, type(form.instance)
        form.instance.owner = self.request.user
        return super(PostListingView, self).form_valid(form)


class ReplyListingView(CreateView):
    model = ContactMessage
    form_class = CreateContactMessageForm
    success_url = "/listing/"

    def get_initial(self):
        d = super(ReplyListingView, self).get_initial()
        listing_id = self.kwargs.get('pk')
        listing_obj = Listing.objects.get(id=int(listing_id))
        d['msg_title'] = listing_obj.title
        return d

    def get_context_data(self, **kwargs):
        d = super(ReplyListingView, self).get_context_data(**kwargs)
        d['msg_sender'] = self.request.user
        listing_id = self.kwargs.get('pk')
        listing_obj = Listing.objects.get(id=int(listing_id))
        d['msg_receiver'] = listing_obj.owner
        d['listing_title'] = listing_obj.title
        d['listing_id'] = listing_id
        d['action_type'] = listing_obj.get_complement_action()
        d['action_preposition'] = listing_obj.get_complement_preposition()
        return d

    def form_valid(self, form):
        # assert False, type(form.instance)
        #TODO send mail with GMAIL
        listing_id = self.kwargs.get('pk')
        listing_obj = Listing.objects.get(id=int(listing_id))
        self.success_url = '/listing/'+listing_id
        form.instance.msg_sender = self.request.user
        form.instance.msg_receiver = listing_obj.owner
        form.instance.listing = listing_obj
        send_mail(
            subject=form.cleaned_data.get('msg_title').strip(),
            message=form.cleaned_data.get('msg_body').strip(),
            from_email=self.request.user.email, #'contact-form@myapp.com',
            recipient_list=[listing_obj.owner.email],
        )
        return super(ReplyListingView, self).form_valid(form)
