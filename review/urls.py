from django.urls import path
from core.views import HomeView
from review import views
from review.views import TicketCreateView, ReviewCreateView, TicketListView




urlpatterns = [
    path('', HomeView.as_view(template_name='core/base.html'), name ="home"),
    path('posts/', TicketCreateView.as_view(template_name='review/ticket.html'), name="create_ticket"),
    path('flux/',views.flux_view, name="flux"),
    path('reviews/create/',ReviewCreateView.as_view(template_name='review/review_form.html'), name="create_review"), 
    path('add_review/<int:id_ticket>', views.add_review, name="add_review"), 
    path('subscription/', views.subscription, name="subscription"), 
    

]





