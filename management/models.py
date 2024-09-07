from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User


class Material(models.Model):
    STATUS_CHOICES = [
        ('new', 'Жаңа'),
        ('used', 'Қолданылған')
    ]
    name = models.CharField(max_length=200, verbose_name='Атауы')
    model_compatibility = models.CharField(max_length=200, verbose_name='Үйлесімділік моделі')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Күйі')
    expiration_date = models.DateField(blank=True, null=True, verbose_name='Жарамдылық мерзімі')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Бағасы')
    quantity = models.IntegerField(verbose_name='Саны')

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалдар'

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Қызмет атауы')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Бағасы')
    materials_required = models.ManyToManyField(Material, through='ServiceMaterial', verbose_name='Қажет материалдар')

    class Meta:
        verbose_name = 'Қызмет'
        verbose_name_plural = 'Қызметтер'

    def __str__(self):
        return self.name

class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=200, verbose_name='Техник аты')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Қызмет')
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Қызмет ақысы', default=10000.00)

    class Meta:
        verbose_name = 'Техник'
        verbose_name_plural = 'Техниктер'

    def __str__(self):
        return f"{self.name} ({self.service.name})"


class ServiceMaterial(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Қызмет')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Материал')
    quantity_required = models.IntegerField(verbose_name='Қажет саны')

    class Meta:
        verbose_name = 'Қызмет бойынша материал'
        verbose_name_plural = 'Қызметтер бойынша материалдар'
        unique_together = ('service', 'material')


class Order(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('repair', 'Ремонт'),
        ('upgrade', 'Модернизация')
    ]
    STATUS_CHOICES = [
        ('submitted', 'Подан'),
        ('processing', 'Обрабатывается'),
        ('completed', 'Завершён'),
        ('canceled', 'Отменён')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted', verbose_name='Күй')
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES, verbose_name='Қызмет түрі')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Қызмет')
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, verbose_name='Техник')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name='Өзіндік құны')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name='Сату бағасы')
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False, verbose_name='Пайда')
    description = models.TextField(verbose_name='Мәселе/сұраныс сипаттамасы')
    completion_date = models.DateField(verbose_name='Аяқталу күні')
    materials_used = models.ManyToManyField(Material, through='OrderMaterial', editable=False, verbose_name='Қолданылған материалдар')

    def save(self, *args, **kwargs):
        # Проверяем, новый ли это заказ (нет id)
        is_new = self._state.adding

        if is_new:
            # Инициализация начального значения с Decimal
            materials_cost = Decimal('0.00')

            # Убедимся, что все операции производятся с Decimal
            for sm in ServiceMaterial.objects.filter(service=self.service):
                materials_cost += sm.material.price * Decimal(sm.quantity_required)

            technician_fee = Decimal(self.technician.service_fee)  # Приведение типа

            # Расчет себестоимости и продажной цены
            self.cost_price = materials_cost + technician_fee
            self.sale_price = Decimal(self.service.price)
            self.profit = self.sale_price - self.cost_price

        super().save(*args, **kwargs)  # Сохраняем заказ с уже расчитанными значениями

        if is_new:
            # Добавление используемых материалов в заказ
            for sm in ServiceMaterial.objects.filter(service=self.service):
                OrderMaterial.objects.create(order=self, material=sm.material, quantity_used=sm.quantity_required)

            # Создание транзакции
            Transaction.objects.create(
                order=self,
                transaction_type='income',
                amount=self.profit,
                comment='Profit from order'
            )

    class Meta:
        verbose_name = 'Тапсырыс'
        verbose_name_plural = 'Тапсырыстар'

    def __str__(self):
        return f"Order {self.id} - {self.service.name}"

class OrderMaterial(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Тапсырыс')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Материал')
    quantity_used = models.IntegerField(verbose_name='Қолданылған саны')

    class Meta:
        verbose_name = 'Тапсырыс бойынша материал'
        verbose_name_plural = 'Тапсырыстар бойынша материалдар'

    def save(self, *args, **kwargs):
            if not self.pk:  # Only decrease quantity on creation
                self.material.quantity -= self.quantity_used
                self.material.save()
            super().save(*args, **kwargs)

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Кіріс'),
        ('expense', 'Шығыс')
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Тапсырыс')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, verbose_name='Транзакция түрі')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сомасы')
    comment = models.TextField(verbose_name='Пікір')
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'),
                                          verbose_name='Ағымдағы баланс')

    def save(self, *args, **kwargs):
        # Убедимся, что current_balance и amount оба Decimal
        if not hasattr(self, 'current_balance') or self.current_balance is None:
            self.current_balance = Decimal('0.00')  # Инициализация, если не установлено

        self.current_balance = Decimal(self.current_balance)  # Приведение типа, на всякий случай

        if not self.pk:  # Проверяем, новая ли это транзакция
            if self.transaction_type == 'income':
                self.current_balance += Decimal(self.amount)
            elif self.transaction_type == 'expense':
                self.current_balance -= Decimal(self.amount)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакциялар'

    def __str__(self):
        return f"{self.transaction_type} of {self.amount}"

