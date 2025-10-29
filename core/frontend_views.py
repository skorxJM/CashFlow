# core/frontend_views.py
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

def dashboard_page(request):
    return render(request, 'dashboard.html')

def transactions_list_page(request):
    return render(request, 'transactions_list.html')

def transaction_new_page(request):
    return render(request, 'transaction_new.html')

def transaction_edit_page(request, tx_id):
    return render(request, 'transaction_edit.html', {'tx_id': tx_id})

def transaction_delete_page(request, tx_id):
    return render(request, 'transaction_delete.html', {'tx_id': tx_id})

def categories_list_page(request):
    return render(request, 'categories_list.html')

def category_new_page(request):
    return render(request, 'category_new.html')

def category_edit_page(request, cat_id):
    return render(request, 'category_edit.html', {'cat_id': cat_id})

def export_page(request):
    return render(request, 'export.html')

# Simple registration view (minimal)
@require_http_methods(["GET","POST"])
def register_page(request):
    if request.method == "POST":
        # placeholder: en el futuro crear usuario; por ahora redirige al login
        return redirect('/accounts/login/')
    return render(request, 'register.html')
