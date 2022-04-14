from django.urls import path, re_path
from . import views

app_name = 'bereket'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('product_list/', views.product_list, name="product_list"),
    path('add_product/', views.add_product, name="add_product"),
    path('edit_product/<int:product_id>', views.edit_product, name="edit_product"),
    path('installment/', views.installment, name="installment"),
    path('clients/', views.get_clients, name="clients"),
    path('clients/<int:client_id>/', views.get_client_detail, name="client_detail"),
    path('cash/', views.cash, name="cash"),
    path('sales/', views.sales, name="sales"),
    path('add_transaction/<int:client_id>/<int:sale_id>/', views.add_transaction, name="add_transaction"),
    path('installment_for_exist_client/<int:client_id>', views.installment_for_exist_client, name="installment_for_exist_client"),
    path('add_consumption/', views.add_consumption, name='add_consumption')
]