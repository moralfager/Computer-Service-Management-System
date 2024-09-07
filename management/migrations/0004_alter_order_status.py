# Generated by Django 4.2.11 on 2024-04-29 02:14
from _decimal import Decimal
from django.db import migrations, models

def create_materials(apps, schema_editor):
    Material = apps.get_model('management', 'Material')
    Material.objects.bulk_create([
        Material(name='Теплопаста', model_compatibility='Standard', status='new', price=Decimal('5.00'), quantity=20),
        Material(name='Вентиляторы', model_compatibility='Standard', status='new', price=Decimal('10.00'), quantity=20),
        Material(name='Термопрокладки', model_compatibility='Standard', status='new', price=Decimal('3.00'), quantity=20),

        Material(name='Радиаторы', model_compatibility='Standard', status='new', price=Decimal('15.00'),
                 quantity=20),
        Material(name='Термопленка для охлаждения', model_compatibility='Standard', status='new',
                 price=Decimal('2.50'), quantity=20),
        Material(name='Шпильки для крепления радиаторов', model_compatibility='Standard', status='new',
                 price=Decimal('1.50'), quantity=20),
        Material(name='Болты и гайки для крепления кулеров', model_compatibility='Standard', status='new',
                 price=Decimal('1.00'), quantity=20),
        Material(name='Очиститель для удаления пыли', model_compatibility='Standard', status='new',
                 price=Decimal('8.00'), quantity=20),
        Material(name='Компрессор для сжатого воздуха', model_compatibility='Standard', status='new',
                 price=Decimal('50.00'), quantity=20),
        Material(name='Зажимы для кабелей', model_compatibility='Standard', status='new', price=Decimal('0.50'),
                 quantity=20),
        Material(name='Пластиковые держатели кабелей', model_compatibility='Standard', status='new',
                 price=Decimal('0.30'), quantity=20),
        Material(name='Термоэлектрические охладители', model_compatibility='Standard', status='new',
                 price=Decimal('25.00'), quantity=20),
        Material(name='Кулеры для систем охлаждения воды', model_compatibility='Standard', status='new',
                 price=Decimal('40.00'), quantity=20),
        Material(name='Резиновые прокладки для уплотнения соединений', model_compatibility='Standard', status='new',
                 price=Decimal('0.80'), quantity=20),
        Material(name='Водяные трубки для систем охлаждения водой', model_compatibility='Standard', status='new',
                 price=Decimal('3.00'), quantity=20),
        Material(name='Жидкость для охлаждения', model_compatibility='Standard', status='new',
                 price=Decimal('10.00'), quantity=20),
        Material(name='Термоподушки', model_compatibility='Standard', status='new', price=Decimal('3.50'),
                 quantity=20),
        Material(name='Клей для крепления радиаторов и кулеров', model_compatibility='Standard', status='new',
                 price=Decimal('5.00'), quantity=20),
        Material(name='Силиконовые прокладки', model_compatibility='Standard', status='new', price=Decimal('1.20'),
                 quantity=20),
        Material(name='Термоэлектрические пластины', model_compatibility='Standard', status='new',
                 price=Decimal('18.00'), quantity=20),
        ])

class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_alter_technician_service_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('submitted', 'Подан'), ('processing', 'Обрабатывается'), ('completed', 'Завершён'), ('canceled', 'Отменён')], default='submitted', max_length=10, verbose_name='Күй'),
        ),
        migrations.RunPython(create_materials),
    ]
