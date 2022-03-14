from django.urls import path
from core.views import HomeView
from review import views
from review.views import TicketCreateView, ReviewCreateView, TicketDeleteView, TicketUpdateView, ReviewDeleteView, ReviewUpdateView




urlpatterns = [
    path('', HomeView.as_view(template_name='core/base.html'), name ="home"),
    path('posts/', views.my_post_view, name="my_posts"),
    path('flux/',views.flux_view, name="flux"),
    path('reviews/create/',views.create_review_and_create_ticket, name="create_review"),
    path('add_review/<int:id_ticket>', ReviewCreateView.as_view() , name="add_review"),
    path('create_ticket/', TicketCreateView.as_view(template_name='review/ticket.html'), name="create_ticket"),
    path('subscription/', views.subscription, name="subscription"),
    path('delete/ticket/<int:pk>', TicketDeleteView.as_view(), name='ticket_delete'),
    path('update/ticket/<int:pk>', TicketUpdateView.as_view(), name='ticket_update'),
    path('delete/review/<int:pk>', ReviewDeleteView.as_view(), name='review_delete'),
    path('update/review/<int:pk>', ReviewUpdateView.as_view(), name='review_update'),
]





