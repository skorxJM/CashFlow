from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer, RegisterSerializer
from django.contrib.auth import authenticate
from django.http import JsonResponse

# Re-exportar register_view desde frontend_views; si no existe, proveer un fallback simple
try:
    from .frontend_views import register_view  # <-- re-exportar para compatibilidad con backend/urls.py
except (ImportError, AttributeError):
    def register_view(request):
        return render(request, "register.html")

# Definir una clase base para compartir configuraciones comunes
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]  # <- en producción cambiar a IsAuthenticated

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
class TransactionViewSet(BaseViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)

class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health(request):
    return Response({"status": "ok"})

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def debug_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    return JsonResponse({
        'user_exists': User.objects.filter(username=username).exists(),
        'authentication_successful': user is not None,
    })