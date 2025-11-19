"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core.views import (
    TransactionViewSet, 
    CategoryViewSet, 
    health,
    RegisterView,
    debug_login  # Añade esta importación
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
# backend/urls.py (fragmento superior)
from core.frontend_views import (
    dashboard_page,
    transactions_list_page,
    transaction_new_page,
    transaction_edit_page,
    transaction_delete_page,
    categories_list_page,
    category_new_page,
    category_edit_page,
    category_delete_page,
    export_page,
    register_page,
)

router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'categories', CategoryViewSet, basename='categories')



urlpatterns = [
    path('', dashboard_page, name='home'),
    path('transactions/', transactions_list_page, name='transactions_list'),
    path('transactions/new/', transaction_new_page, name='transaction_new'),
    path('transactions/<int:tx_id>/edit/', transaction_edit_page, name='transaction_edit'),
    path('transactions/<int:tx_id>/delete/', transaction_delete_page, name='transaction_delete'),
    
    path('categories/', categories_list_page, name='categories_list'),
    path('categories/new/', category_new_page, name='category_new'),
    path('categories/<int:cat_id>/edit/', category_edit_page, name='category_edit'),
    path('categories/<int:cat_id>/delete/', category_delete_page, name='category_delete'),
    path('export/', export_page, name='export'),
    
    path('accounts/register/', register_page, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('admin/', admin.site.urls),
    
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/debug-login/', debug_login, name='debug_login'),
    
    path('health/', health, name='health'),
]
