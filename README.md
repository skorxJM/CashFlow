Cashflow
# 💰 CashFlow

Aplicación web para gestionar ingresos y gastos personales.  
Desarrollada con **Django REST Framework + Tailwind/React + PostgreSQL**.

# 📂 Mapa de documentación

La documentación inicial se encuentra organizada en la carpeta docs/ y las decisiones arquitectónicas en adr/.

    docs/01-vision-alcance.md → Acta de visión y alcance.

    docs/02-nfrs.md → Catálogo de requerimientos no funcionales.

    docs/03-c4-contexto-contenedores.md → Diseño C4 (contexto y contenedores).

    docs/04-backlog.md → Backlog inicial con historias INVEST.

    adr/ADR-000-monolito-django-postgres.md → Decisión arquitectónica inicial.

## 🗂️ Estructura de carpetas
```
├── adr
│   ├── ADR-000-monolito-node-postgres.md
│   ├── ADR-001-base-de-datos.md
│   └── ADR-002-autenticacion-jwt.md
├── backend
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   ├── settings.cpython-313.pyc
│   │   ├── urls.cpython-313.pyc
│   │   └── wsgi.cpython-313.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── frontend_views.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-313.pyc
│   │       └── __init__.cpython-313.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-313.pyc
│   │   ├── apps.cpython-313.pyc
│   │   ├── frontend_views.cpython-313.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── models.cpython-313.pyc
│   │   ├── serializers.cpython-313.pyc
│   │   └── views.cpython-313.pyc
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
├── db.sqlite3
├── docs
│   ├── 01-vision-alcance.md
│   ├── 02-nfrs.md
│   └── 03-backlog.md
├── LICENSE
├── manage.py
├── README.md
├── requirements.txt
└── templates
    ├── base.html
    ├── categories_list.html
    ├── category_edit.html
    ├── category_new.html
    ├── dashboard.html
    ├── export.html
    ├── login.html
    ├── register.html
    ├── transaction_delete.html
    ├── transaction_edit.html
    ├── transaction_new.html
    ├── transactions.html
    └── transactions_list.html
```


