from django.urls import path
from . import views
urlpatterns=[
    path('',views.movie_list,name='movie_list'),
    path('<int:movie_id>/theaters',views.theater_list,name='theater_list'),
    path('theater/<int:theater_id>/seats/book/',views.book_seats,name='book_seats'),
    path('theater/<int:theater_id>/checkout/', views.checkout, name='checkout'),
    path('theater/<int:theater_id>/confirm/', views.confirm_booking, name='confirm_booking'),
    path('theater/<int:theater_id>/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('theater/<int:theater_id>/payment_success/', views.payment_success, name='payment_success'),
    path('theater/<int:theater_id>/payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('theater/<int:theater_id>/status/', views.check_seat_status, name='check_seat_status'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]