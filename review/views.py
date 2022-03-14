from datetime import datetime
from django.db.models import Value, CharField
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import TicketForm, ReviewForm
from .models import Review, Ticket
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
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
    model = Ticket
    template_name = 'review/ticket_update.html'
    fields = [
            'title',
            'description',
            'image',
            'user',
        ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.time_created = datetime
        return super().form_valid(form)

    def test_func(self):
        post =self.get_object()
        if self.request.user == post.user:
            return True
        raise PermissionDenied

class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('home')

    def test_func(self):
        post =self.get_object()
        if self.request.user == post.user:
            return True
        raise PermissionDenied

def flux_view(request):
    tickets = Ticket.objects.filter(user__in=request.user.following.all()).annotate(type=Value('ticket', CharField())).union(Ticket.objects.filter(user=request.user).annotate(type=Value('ticket', CharField())))
    for ticket in tickets:
        ticket.is_closed = ticket.is_already_reviewed(request.user)

    reviews = Review.objects.filter(user__in=request.user.following.all()).annotate(type=Value('review', CharField())).union(Review.objects.filter(user=request.user).annotate(type=Value('review', CharField())))
    results = list(tickets) + list(reviews)
    results.sort(key=lambda d: d.time_created, reverse=True)
    for result in results:
        print(result.__dict__)
    context = {
                'results': results
            }
    return render(request, 'review/flux.html', context)

def my_post_view(request):
    tickets = Ticket.objects.filter(user=request.user).annotate(type=Value('ticket', CharField())).union(Ticket.objects.filter(user=request.user).annotate(type=Value('ticket', CharField())))
    for ticket in tickets:
        ticket.is_closed = ticket.is_already_reviewed(request.user)

    reviews = Review.objects.filter(user=request.user).annotate(type=Value('review', CharField())).union(Review.objects.filter(user=request.user).annotate(type=Value('review', CharField())))
    results = list(tickets) + list(reviews)
    results.sort(key=lambda d: d.time_created)

    context = {
                'results': results
            }
    return render(request, 'review/my_posts.html', context)

class ReviewCreateView(LoginRequiredMixin, CreateView):
    template_name = "review/review_form_without_ticket.html"
    form_class = ReviewForm
    model = Review
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ticket = Ticket.objects.get(id=self.kwargs['id_ticket'])
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = Ticket.objects.get(id=self.kwargs['id_ticket'])
        return context

class ReviewUpdateView(UpdateView):
  model = Review
  template_name = 'review/review_update.html'
  fields = [
            "headline",
            "rating",
            "body",
        ]

class ReviewDeleteView(DeleteView):
  model = Review
  template_name = 'review/review_confirm_delete.html'
  success_url = reverse_lazy('home')

def create_review_and_create_ticket(request):
    review_form = ReviewForm() 
    ticket_form = TicketForm()
  
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        review_form = ReviewForm(request.POST)
        if review_form.is_valid() and ticket_form.is_valid():
            ticket_form.instance.user = request.user
            review_form.instance.user = request.user
            ticket = ticket_form.save()
            review_form.instance.ticket = ticket
            review_form.save()
            return redirect('home') 
        else:
            print(review_form)

    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request,'review/edit_review.html', context=context)

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