# core/frontend_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction, Category, ExportReport
from decimal import Decimal, InvalidOperation
from django.db.models import Sum, Q
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import datetime
import json
import csv
from io import BytesIO
from django.utils.dateparse import parse_datetime

# Importa la función que genera el PDF desde tu módulo separado
# (asegúrate de que core/pdf_reports.py esté en la misma app 'core')
from .pdf_reports import generate_pdf as generate_pdf_report


@require_http_methods(["GET"])
@login_required
def dashboard_page(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    # Calcular totales
    total_income = Transaction.objects.filter(
        user=request.user, 
        type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    total_expense = Transaction.objects.filter(
        user=request.user, 
        type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    balance = total_income - total_expense
    
    # Transacciones por categoría (top 5)
    categories_summary = Category.objects.filter(user=request.user).annotate(
        total=Sum('transactions__amount')
    ).order_by('-total')[:5]
    
    return render(request, 'dashboard.html', {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'categories_summary': categories_summary,
    })


@require_http_methods(["GET"])
@login_required
def transactions_list_page(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'transactions_list.html', {
        'transactions': transactions,
        'categories': categories,
    })


@require_http_methods(["GET", "POST"])
@login_required
def transaction_new_page(request):
    categories = Category.objects.filter(user=request.user)

    # Valor por defecto para el campo datetime-local
    current_datetime = timezone.now().strftime("%Y-%m-%dT%H:%M")

    if request.method == "POST":
        description = request.POST.get('description', '').strip()
        amount_raw = request.POST.get('amount', '').strip()
        category_id = request.POST.get('category')
        tx_type = request.POST.get('type', 'expense')
        created_at_str = request.POST.get("created_at")

        # Validar monto
        try:
            amount = Decimal(amount_raw)
        except (InvalidOperation, TypeError, ValueError):
            messages.error(request, "Importe inválido.")
            return render(
                request,
                'transaction_new.html',
                {
                    'categories': categories,
                    'current_datetime': current_datetime
                }
            )
        
        # Categoría opcional
        category = None
        if category_id:
            category = get_object_or_404(Category, pk=category_id, user=request.user)

        # Fecha personalizada
        if created_at_str:
            try:
                created_at = datetime.fromisoformat(created_at_str)
            except ValueError:
                created_at = timezone.now()
        else:
            created_at = timezone.now()

        # Crear transacción
        Transaction.objects.create(
            user=request.user,
            type=tx_type,
            amount=amount,
            category=category,
            description=description,
            created_at=created_at
        )

        messages.success(request, "Transacción creada correctamente.")
        return redirect('transactions_list')

    # GET → Render con current_datetime
    return render(
        request,
        'transaction_new.html',
        {
            'categories': categories,
            'current_datetime': current_datetime
        }
    )



@require_http_methods(["GET", "POST"])
@login_required
def transaction_edit_page(request, tx_id):
    tx = get_object_or_404(Transaction, pk=tx_id, user=request.user)
    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        description = request.POST.get('description', '').strip()
        amount_raw = request.POST.get('amount', '').strip()
        category_id = request.POST.get('category')
        tx_type = request.POST.get('type', 'expense')
        created_at_str = request.POST.get('created_at')

        # Validar monto
        try:
            amount = Decimal(amount_raw)
        except (InvalidOperation, TypeError, ValueError):
            messages.error(request, "Importe inválido.")
            # repoblar el campo created_at si venía en POST para no perderlo
            context = {
                'transaction': tx,
                'categories': categories,
                'created_at_value': created_at_str or tx.created_at.strftime("%Y-%m-%dT%H:%M")
            }
            return render(request, 'transaction_edit.html', context)

        # Categoría opcional
        category = None
        if category_id:
            category = get_object_or_404(Category, pk=category_id, user=request.user)

        # Parsear created_at de forma robusta y asegurar tz-aware
        if created_at_str:
            dt = parse_datetime(created_at_str)
            if dt is None:
                try:
                    dt = datetime.fromisoformat(created_at_str)
                except Exception:
                    dt = timezone.now()
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt, timezone.get_current_timezone())
            created_at = dt
        else:
            created_at = tx.created_at  # mantener la fecha actual si no se envía

        # Actualizar la transacción
        tx.description = description
        tx.amount = amount
        tx.category = category
        tx.type = tx_type
        tx.created_at = created_at
        tx.save()

        messages.success(request, "Transacción actualizada correctamente.")
        return redirect('transactions_list')

    # GET: pasar valor formateado para el input datetime-local si lo necesitas
    context = {
        'transaction': tx,
        'categories': categories,
        'created_at_value': tx.created_at.strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, 'transaction_edit.html', context)



@require_http_methods(["GET", "POST"])
@login_required
def transaction_delete_page(request, tx_id):
    tx = get_object_or_404(Transaction, pk=tx_id, user=request.user)
    
    if request.method == "POST":
        tx.delete()
        messages.success(request, "Transacción eliminada correctamente.")
        return redirect('transactions_list')
    
    return render(request, 'transaction_delete.html', {'transaction': tx})


@require_http_methods(["GET", "POST"])
@login_required
def categories_list_page(request):
    categories = Category.objects.filter(user=request.user).order_by('name')
    return render(request, 'categories_list.html', {'categories': categories})


@require_http_methods(["GET", "POST"])
@login_required
def category_new_page(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        
        if not name:
            messages.error(request, "El nombre de la categoría es obligatorio.")
            return render(request, 'category_new.html')
        
        if Category.objects.filter(user=request.user, name=name).exists():
            messages.error(request, "Ya existe una categoría con ese nombre.")
            return render(request, 'category_new.html')
        
        try:
            Category.objects.create(user=request.user, name=name)
            messages.success(request, f"Categoría '{name}' creada correctamente.")
            return redirect('categories_list')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, 'category_new.html')
    
    return render(request, 'category_new.html')


@require_http_methods(["GET", "POST"])
@login_required
def category_edit_page(request, cat_id):
    category = get_object_or_404(Category, pk=cat_id, user=request.user)
    
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        
        if not name:
            messages.error(request, "El nombre es obligatorio.")
            return render(request, 'category_edit.html', {'category': category})
        
        category.name = name
        category.save()
        messages.success(request, "Categoría actualizada correctamente.")
        return redirect('categories_list')
    
    return render(request, 'category_edit.html', {'category': category})


@require_http_methods(["GET", "POST"])
@login_required
def category_delete_page(request, cat_id):
    category = get_object_or_404(Category, pk=cat_id, user=request.user)
    
    if request.method == "POST":
        name = category.name
        category.delete()
        messages.success(request, f"Categoría '{name}' eliminada.")
        return redirect('categories_list')
    
    return render(request, 'category_delete.html', {'category': category})


@require_http_methods(["GET", "POST"])
@login_required
def export_page(request):
    if request.method == "POST":
        start_date_str = request.POST.get('start')
        end_date_str = request.POST.get('end')
        export_format = request.POST.get('format', 'csv')
        
        # Validar fechas
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        except ValueError:
            messages.error(request, "Formato de fecha inválido.")
            return redirect('export')
        
        # Filtrar transacciones
        transactions = Transaction.objects.filter(user=request.user)
        
        if start_date:
            transactions = transactions.filter(created_at__date__gte=start_date)
        if end_date:
            transactions = transactions.filter(created_at__date__lte=end_date)
        
        transactions = transactions.order_by('-created_at')
        
        # Crear registro del informe
        report_name = f"Informe {export_format.upper()} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        report = ExportReport.objects.create(
            user=request.user,
            name=report_name,
            format=export_format,
            start_date=start_date,
            end_date=end_date,
            transactions_count=transactions.count()
        )
        
        if export_format == 'csv':
            return generate_csv(request.user, transactions, start_date, end_date)
        elif export_format == 'json':
            return generate_json(request.user, transactions, start_date, end_date)
        elif export_format == 'pdf':
            # Llamada delegada al servicio que genera el PDF
            result = generate_pdf_report(request.user, transactions, start_date, end_date)
            # Si la función ya devolvió un HttpResponse, lo devolvemos tal cual
            if isinstance(result, HttpResponse):
                return result
            # Si devolvió un BytesIO-like o bytes, construimos la respuesta aquí
            if hasattr(result, 'getvalue'):  # BytesIO
                content = result.getvalue()
            elif isinstance(result, (bytes, bytearray)):
                content = bytes(result)
            else:
                # Caso fallback: intentar convertir a str (no esperado)
                content = str(result).encode('utf-8')
            filename = f"informe_{request.user.username}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            response = HttpResponse(content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    
    # GET: mostrar formulario y últimos 3 informes
    recent_reports = ExportReport.objects.filter(user=request.user).order_by('-created_at')[:3]
    
    return render(request, 'export.html', {
        'recent_reports': recent_reports,
    })


def generate_csv(user, transactions, start_date, end_date):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="informe_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Tipo', 'Monto', 'Categoría', 'Descripción'])
    
    for tx in transactions:
        writer.writerow([
            tx.created_at.strftime('%Y-%m-%d %H:%M'),
            'Ingreso' if tx.type == 'income' else 'Gasto',
            tx.amount,
            tx.category.name if tx.category else '',
            tx.description,
        ])
    
    # Agregar resumen
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    writer.writerow([])
    writer.writerow(['RESUMEN'])
    writer.writerow(['Ingresos totales:', total_income])
    writer.writerow(['Gastos totales:', total_expense])
    writer.writerow(['Balance:', total_income - total_expense])
    
    return response


def generate_json(user, transactions, start_date, end_date):
    data = {
        'usuario': user.username,
        'fecha_generacion': datetime.now().isoformat(),
        'periodo': {
            'desde': start_date.isoformat() if start_date else None,
            'hasta': end_date.isoformat() if end_date else None,
        },
        'transacciones': [],
        'resumen': {}
    }
    
    for tx in transactions:
        data['transacciones'].append({
            'fecha': tx.created_at.isoformat(),
            'tipo': tx.type,
            'monto': float(tx.amount),
            'categoria': tx.category.name if tx.category else None,
            'descripcion': tx.description,
        })
    
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    data['resumen'] = {
        'ingresos_totales': float(total_income),
        'gastos_totales': float(total_expense),
        'balance': float(total_income - total_expense),
        'total_transacciones': transactions.count(),
    }
    
    response = HttpResponse(json.dumps(data, indent=2, default=str), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="informe_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"'
    
    return response


def get_recent_reports(user):
    """Obtener los últimos 3 informes del usuario"""
    return ExportReport.objects.filter(user=user).order_by('-created_at')[:3]


@require_http_methods(["GET", "POST"])
def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'register.html')
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, "Registro exitoso.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, 'register.html')
    
    return render(request, 'register.html')
