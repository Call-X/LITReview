from datetime import datetime
from operator import attrgetter
from urllib import request
from django.core.paginator import Paginator



from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, TemplateView
import datetime

from django.contrib.auth.models import User

from core.models import User
import review

from .forms import TicketForm, ReviewForm
from .models import Review, Ticket
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Ticket, Review


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = "review/ticket.html"
    form_class = TicketForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = reverse_lazy("home")


class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    models = Ticket
    fields = ['title', 'description', 'image']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.time_created = datetime
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user == self.get_object().user


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user == self.get_object().user   

    def get_queryset(self):
        return Ticket.objects.order_by('id')


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket

def flux_view(request):
    
#  user__in=request.user.following.all()
    tickets = Ticket.objects.all()
    for ticket in tickets:
        ticket.is_closed = ticket.is_already_reviewed(request.user)
    reviews = Review.objects.filter(user__in=request.user.following.all())
    context = {
                'tickets': tickets,
                'reviews' : reviews  
            }
    return render(request, 'review/flux.html', context)


def detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    context = {
        'ticket_title': ticket.title,
        'ticket_id': id,
        'thumbnail': ticket.image
    }

    return render(request,'review/ticket_card.html', context)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    
    template_name = "review/review_form.html"
    form_class = ReviewForm
    model = Review

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = reverse_lazy("home")

class ReviewUpdate(UpdateView):
  model = Review

class ReviewDelete(DeleteView):
  model = Review
  success_url = reverse_lazy('home')


def add_review(request, id_ticket=None):

    if id_ticket is not None:
        ticket = get_object_or_404(Ticket, pk=id_ticket)
        review = Review.objects.filter(ticket=ticket, user=request.user).exists()
        if review:
            return redirect('ticket_list')
    else:
        return redirect('ticket_list')


    if request.method == "GET":
            review_form = ReviewForm()
            context = {
                'ticket': ticket,
                'review_form': review_form,   
            }
            return render(request, 'review/review_form.html', context)

    elif request.method == 'POST':
        review_form = ReviewForm(request.POST)
        review_form.instance.user = request.user
        review_form.instance.ticket = ticket

        if review_form.is_valid():

            review_form.save()
            return redirect('ticket_list')
        else:
            context = {
                'ticket': ticket,
                'review_form': review_form,
            }

            return render(request, 'review/review_form.html', context)
    else:
        return redirect('ticket_list')


def subscription(request):
    followers = request.user.following.all()
    follow_list = []

    for user in User.objects.all():
        if user not in followers and user != request.user:
            follow_list.append(user)

    if request.method == 'POST':
        if request.POST.get('followed_user'):
            request.user.following.add(User.objects.get(pk=request.POST['followed_user']))
        elif request.POST.get('delete'):
            request.user.following.remove(User.objects.get(id=request.POST['delete']))

        return redirect('subscription')

    context = {
            'follow_list':follow_list,
            'followers': followers,
            'followed_by': request.user.followed_by(),
        }
    return render(request, 'review/subscription_form.html', context)






















# class FeedsView(LoginRequiredMixin, TemplateView):
    
#     context_name = 'flux_news'
#     view_type = 'flux'

#     def get_flux_news(self):
#         tickets = list(Ticket.objects.all())
#         reviews = list(Review.objects.all())
#         followed_users = [object.followed_user
#                           for object in User.objects.all()
#                           if object.following == self.request.user]

#         tickets = [ticket for ticket in tickets
#                    if (ticket.user in followed_users)
#                    or (ticket.user == self.request.user)]
#         reviews = [review for review in reviews
#                    if ((review.user in followed_users)
#                        or (review.user == self.request.user)
#                        or (review.ticket.user in followed_users)
#                        or (review.ticket.user == self.request.user))]
#         feeds_news = tickets + reviews
#         feeds_news.sort(key=attrgetter('time_created'), reverse=True)
#         return feeds_news
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         flux_news = self.get_flux_news()

#         paginator = Paginator(flux_news, 5)
#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         context['page_obj'] = page_obj
#         context['rating_range'] = Review.get_rating_range()

#         return context
