import datetime
from datetime import date

import pytz
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .forms import LoginForm, ClientForm, SaleForm, TransactionForm, CashForm, ProductForm, ConsumptionForm
from .models import Product, Sale, Client, Transaction, Cash, Consumption


def user_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('bereket:product_list')
                else:
                    return render(request, 'Home.html', {'form': form, 'errors': 'Disabled account'})
            else:
                return render(request, 'Home.html', {'form': form, 'errors': 'Invalid login'})

    return render(request, 'Home.html', {'form': form})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return redirect('bereket:login')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):
    products = Product.objects.all().order_by("-id")
    return render(request, 'Page-1.html', {'products': products})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    product_form = ProductForm()
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            return redirect('bereket:product_list')
        error = product_form.errors
        return render(request, 'add_product.html', {'product_form': product_form, 'error': error})
    return render(request, 'add_product.html', {'product_form': product_form})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def edit_product(request, product_id):
    product = Product.objects.filter(pk=product_id).first()
    product_form = ProductForm(instance=product)
    if request.method == 'POST':
        product_form = ProductForm(instance=product, data=request.POST)
        if product_form.is_valid():
            product_form.save()
            return redirect('bereket:product_list')
        error = product_form.errors
        return render(request, 'add_product.html', {'product_form': product_form, 'error': error})
    return render(request, 'edit_product.html', {'product_form': product_form})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def installment(request):
    client_form = ClientForm()
    sale_form = SaleForm()
    products = Product.objects.all()
    if request.method == 'POST':
        product = request.POST['select-1']
        installment_period = request.POST.get('select')
        client_form = ClientForm(request.POST)
        sale_form = SaleForm(request.POST)
        if client_form.is_valid() and sale_form.is_valid():
            product = Product.objects.get(name=product)
            if product.amount <= 0:
                error = 'Данного товара сейчас нет в наличии'
                return render(request, 'installment.html', {'products': products,
                                                            'client_form': client_form,
                                                            'sale_form': sale_form,
                                                            'error':error
                                                            })
            client = client_form.save()
            product.amount = product.amount-1
            product.save()
            client = Client.objects.get(id=client.id)
            sale = Sale(product=product, installment_period=installment_period,
                        first_payment=sale_form.cleaned_data.get("first_payment"),
                        quantity=1,
                        client=client,
                        price=sale_form.cleaned_data.get('price'),
                        rest=sale_form.cleaned_data.get('price')-sale_form.cleaned_data.get("first_payment"))
            sale.save()
            return redirect('bereket:clients')
    return render(request, 'installment.html', {"products": products,
                                                'client_form': client_form,
                                                'sale_form': sale_form,
                                                })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_clients(request):
    clients = Client.objects.all().order_by("-id")
    return render(request, 'client.html', {'clients': clients})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_client_detail(request, client_id):
    client = Client.objects.get(id=client_id)
    sales = Sale.objects.filter(client=client)
    return render(request, 'client_detail.html', {'client': client, 'sales': sales})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cash(request):
    products = Product.objects.all()
    cash_form = CashForm()
    if request.method == 'POST':
        cash_form = CashForm(request.POST)
        if cash_form.is_valid():
            product = request.POST['select-1']
            product = Product.objects.get(name=product)
            if product.amount <= 0:
                error = 'Данного товара сейчас нет в наличии'
                render(request, 'cash.html', {'products': products, 'cash_form': cash_form, 'error':error})
            product.amount = product.amount-1
            product.save()
            cash = Cash(product=product, price=cash_form.cleaned_data.get('price'))
            cash.save()
            return redirect('bereket:sales')
    return render(request, 'cash.html', {'products': products, 'cash_form': cash_form})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sales(request):
    if request.method == 'POST':
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')
        if start_date == '' or end_date == '':
            error = 'Выберите даты!'
            return render(request, 'sales.html', {'summa_of_cash': 0,
                                                  'summa_of_consumption': int(0),
                                                  'total_sales': 0,
                                                  'total': 0,
                                                  'error': error})
        cash = Cash.objects.filter(created_at__range=(datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                                                      datetime.datetime.strptime(end_date, '%Y-%m-%d')))
        sales = Sale.objects.filter(timestamp__range=(datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                                                      datetime.datetime.strptime(end_date, '%Y-%m-%d')))
        transactions = Transaction.objects.filter(created_at__range=(datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                                                                     datetime.datetime.strptime(end_date, '%Y-%m-%d')))
        consumption = Consumption.objects.filter(created_at__range=(datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                                                                    datetime.datetime.strptime(end_date, '%Y-%m-%d')))
    else:
        cash = Cash.objects.all()
        sales = Sale.objects.all()
        transactions = Transaction.objects.all()
        consumption = Consumption.objects.all()
    summa_of_cash = 0
    summa_of_consumption = 0
    for i in cash:
        summa_of_cash += i.price
    for j in consumption:
        summa_of_consumption += j.summa
    total = int(summa_of_cash - summa_of_consumption)
    sales_first_payments = 0
    transactions_payment = 0
    for sale in sales:
        sales_first_payments += sale.first_payment
    for transaction in transactions:
        transactions_payment += transaction.amount
    total_sales = int(sales_first_payments + transactions_payment)
    return render(request, 'sales.html', {'sales': sales,
                                          'consumption': consumption,
                                          'transactions': transactions,
                                          'cash': cash,
                                          'summa_of_cash': summa_of_cash,
                                          'summa_of_consumption': int(summa_of_consumption),
                                          'total_sales': total_sales,
                                          'total': total})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_consumption(request):
    consumption_form = ConsumptionForm()
    if request.method == 'POST':
        consumption_form = ConsumptionForm(request.POST)
        if consumption_form.is_valid():
            consumption_form.save()
            return redirect('bereket:product_list')
    return render(request, 'add_consumption.html', {'consumption_form': consumption_form})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_transaction(request, client_id, sale_id):
    client = Client.objects.get(id=client_id)
    sale = Sale.objects.get(id=sale_id)
    form = TransactionForm()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            summa = form.cleaned_data['payment']
            rest = sale.rest - form.cleaned_data.get("payment")
            if rest < 0:
                error = 'Взнос не может превышать остатка'
                return render(request, 'Add_transaction.html', {'client': client,
                                                                'sale': sale,
                                                                'form': form,
                                                                'error': error
                                                                })
            sale.rest = sale.rest - summa
            transaction = Transaction(sale=sale, amount=summa)
            transaction.save()
            sale.save()
            return redirect('bereket:client_detail', client_id=client_id)
    return render(request, 'Add_transaction.html', {'client': client,
                                                    'sale': sale,
                                                    'form': form})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def installment_for_exist_client(request, client_id):
    client = Client.objects.get(id=client_id)
    sale_form = SaleForm()
    products = Product.objects.all()
    if request.method == 'POST':
        product = request.POST['select-1']
        installment_period = request.POST.get('select')
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            product = Product.objects.get(name=product)
            if product.amount <= 0:
                error = 'Данного товара сейчас нет в наличии'
                return render(request, 'installment_client.html', {'products': products,
                                                            'client': client,
                                                            'sale_form': sale_form,
                                                            'error':error
                                                            })
            product.amount = product.amount -1
            product.save()
            rest = product.price - sale_form.cleaned_data.get("first_payment")
            if rest < 0:
                error = 'Взнос не может превышать остатка. Выберите поля снова'
                return render(request, 'installment_client.html', {'products': products,
                                                                   'sale_form': sale_form,
                                                                   'client': client,
                                                                   'error': error
                                                                   })
            sale = Sale(product=product, installment_period=installment_period,
                        first_payment=sale_form.cleaned_data.get("first_payment"),
                        quantity=1,
                        client=client,
                        price=sale_form.cleaned_data.get('price'),
                        rest=sale_form.cleaned_data.get('price')-sale_form.cleaned_data.get("first_payment"))
            sale.save()
            return redirect('bereket:client_detail', client_id=client.id)
    return render(request, 'installment_client.html', {'products': products,
                                                       'sale_form': sale_form,
                                                       'client': client
                                                       })