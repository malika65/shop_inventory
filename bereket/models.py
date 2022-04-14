from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


class Product(models.Model):
    number = models.IntegerField(verbose_name='Номер(id) товара', unique=True)
    name = models.CharField(max_length=200, verbose_name='Наименование товара', unique=True)
    price = models.IntegerField(verbose_name='Закупочная цена товара')
    amount = models.IntegerField(verbose_name="Количество товара")

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    surname = models.CharField(max_length=200, verbose_name='Фамилия')
    lastname = models.CharField(max_length=200, verbose_name='Отчество')
    passport_id = models.CharField(max_length=200, verbose_name='ID паспорта')
    validity = models.DateTimeField(verbose_name='Срок действия паспорта')
    who_gave = models.CharField(max_length=200, verbose_name='Орган выдачи')
    phone_number = models.CharField(max_length=30, verbose_name='Номер телефона', null=True, blank=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.surname} {self.name}'


class Sale(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Продукт')
    installment_period = models.IntegerField(verbose_name='Срок рассрочки в месяцах')
    first_payment = models.FloatField(verbose_name='Первый взнос')
    quantity = models.IntegerField(default=1, null=True, blank=True, verbose_name='Количество')
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE, verbose_name='ID клиента')
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(verbose_name='Цена продажи', null=True)
    rest = models.PositiveIntegerField(null=True, verbose_name='Остаток выплаты по рассрочке')

    class Meta:
        verbose_name = 'Продажа и рассрочка'
        verbose_name_plural = 'Продажи и рассрочки'

    def __str__(self):
        return f'{self.client}-{self.product}'


class Transaction(models.Model):
    amount = models.FloatField(default=0, verbose_name='Сумма')
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Продажа')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Выплата'
        verbose_name_plural = 'Выплаты'

    def __str__(self):
        return f'{self.sale.client}-{self.created_at.strftime("%d-%m-%Y")}'


class Cash(models.Model):
    price = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Наличные'
        verbose_name_plural = 'Наличные'

    def __str__(self):
        return f'{self.product}-{self.price}'


class Consumption(models.Model):
    who_got = models.CharField(max_length=200, verbose_name='Кто получил')
    summa = models.FloatField(verbose_name='Сколько')
    reason = models.TextField(max_length=500, verbose_name='Причина', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Расходы'
        verbose_name_plural = 'Расходы'

    def __str__(self):
        return f'{self.who_got}-{self.summa}'