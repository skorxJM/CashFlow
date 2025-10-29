from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer

# Definir una clase base para compartir configuraciones comunes
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]  # <- en producción cambiar a IsAuthenticated

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