from django.contrib import admin
from .models import Material, Service, ServiceMaterial, Order, OrderMaterial, Transaction, Technician

admin.site.site_header = 'ServiceART'
admin.site.site_title = 'Компьютерлік техниканы жөндеу және жаңғырту жұмыстарын есепке алу жүйесі'
admin.site.index_title = 'Компьютерлік техниканы жөндеу және жаңғырту жұмыстарын есепке алу жүйесін басқару'

class ServiceMaterialInline(admin.TabularInline):
    model = ServiceMaterial
    extra = 1  # Не показывать пустую форму по умолчанию

class OrderMaterialInline(admin.TabularInline):
    model = OrderMaterial
    extra = 1  # Не показывать пустую форму по умолчанию

class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'service_fee')
    list_filter = ('service',)
    search_fields = ('name', 'service__name')

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_compatibility', 'status', 'expiration_date', 'price', 'quantity')
    list_filter = ('status', 'expiration_date')
    search_fields = ('name', 'model_compatibility')

class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceMaterialInline]
    list_display = ('name', 'price')
    list_filter = ('name',)
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderMaterialInline]
    list_display = ('service', 'technician', 'cost_price', 'sale_price', 'profit', 'completion_date')
    list_filter = ('service', 'technician', 'completion_date')
    search_fields = ('service__name', 'technician__name')
    date_hierarchy = 'completion_date'  # Добавление иерархии по дате для навигации

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'comment', 'order', 'current_balance')
    list_filter = ('transaction_type',)
    search_fields = ('comment', 'order__id')
    date_hierarchy = 'order__completion_date'  # Позволяет фильтровать транзакции по дате выполнения заказа

# Регистрация моделей с использованием расширенных классов администрирования
admin.site.register(Technician, TechnicianAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)
