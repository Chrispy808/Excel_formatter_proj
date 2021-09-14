from django.urls import path     
from . import views
urlpatterns = [
    #GET
    path('', views.index),
    path('dashboard', views.dashboard),
    path('user/edit/<int:User_id>', views.edit_user),
    path('<int:Book_item_name>', views.item),
    path('item/<int:Book_id>/edit', views.edit_item),
    path('item/<str:Book_item_name>', views.all_items),
    path('location/<str:Book_location>', views.locations),
    path('user/<int:User_id>/tracking', views.tracked_items),
    #POST
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('delete_all', views.delete_all),
    path('item/<int:Book_id>/change', views.change_item),
    path('item/<int:Book_id>/delete', views.delete_item),
    path('user/<int:User_id>/change', views.change_user),
    path('<int:Book_id>/track', views.track),
    path('<int:Book_id>/untrack_item_page', views.untrack_item_page),
    path('<int:Book_id>/<int:User_id>/untrack_tracked_page', views.untrack_tracked_page)
]