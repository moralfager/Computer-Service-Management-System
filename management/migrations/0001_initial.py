# Generated by Django 4.2.11 on 2024-04-28 19:56

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Атауы')),
                ('model_compatibility', models.CharField(max_length=200, verbose_name='Үйлесімділік моделі')),
                ('status', models.CharField(choices=[('new', 'Жаңа'), ('used', 'Қолданылған')], max_length=10, verbose_name='Күйі')),
                ('expiration_date', models.DateField(blank=True, null=True, verbose_name='Жарамдылық мерзімі')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Бағасы')),
                ('quantity', models.IntegerField(verbose_name='Саны')),
            ],
            options={
                'verbose_name': 'Материал',
                'verbose_name_plural': 'Материалдар',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('submitted', 'Жіберілді'), ('processing', 'Өңдеу'), ('completed', 'Аяқталды'), ('canceled', 'Бас тартылды')], default='submitted', max_length=10, verbose_name='Күй')),
                ('service_type', models.CharField(choices=[('repair', 'Ремонт'), ('upgrade', 'Модернизация')], max_length=10, verbose_name='Қызмет түрі')),
                ('cost_price', models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='Өзіндік құны')),
                ('sale_price', models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='Сату бағасы')),
                ('profit', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, null=True, verbose_name='Пайда')),
                ('description', models.TextField(verbose_name='Мәселе/сұраныс сипаттамасы')),
                ('completion_date', models.DateField(verbose_name='Аяқталу күні')),
            ],
            options={
                'verbose_name': 'Тапсырыс',
                'verbose_name_plural': 'Тапсырыстар',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Қызмет атауы')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Бағасы')),
            ],
            options={
                'verbose_name': 'Қызмет',
                'verbose_name_plural': 'Қызметтер',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('income', 'Кіріс'), ('expense', 'Шығыс')], max_length=10, verbose_name='Транзакция түрі')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сомасы')),
                ('comment', models.TextField(verbose_name='Пікір')),
                ('current_balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, verbose_name='Ағымдағы баланс')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.order', verbose_name='Тапсырыс')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакциялар',
            },
        ),
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Техник аты')),
                ('service_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Қызмет ақысы')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.service', verbose_name='Қызмет')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Техник',
                'verbose_name_plural': 'Техниктер',
            },
        ),
        migrations.CreateModel(
            name='ServiceMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_required', models.IntegerField(verbose_name='Қажет саны')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.material', verbose_name='Материал')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.service', verbose_name='Қызмет')),
            ],
            options={
                'verbose_name': 'Қызмет бойынша материал',
                'verbose_name_plural': 'Қызметтер бойынша материалдар',
                'unique_together': {('service', 'material')},
            },
        ),
        migrations.AddField(
            model_name='service',
            name='materials_required',
            field=models.ManyToManyField(through='management.ServiceMaterial', to='management.material', verbose_name='Қажет материалдар'),
        ),
        migrations.CreateModel(
            name='OrderMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_used', models.IntegerField(verbose_name='Қолданылған саны')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.material', verbose_name='Материал')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.order', verbose_name='Тапсырыс')),
            ],
            options={
                'verbose_name': 'Тапсырыс бойынша материал',
                'verbose_name_plural': 'Тапсырыстар бойынша материалдар',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='materials_used',
            field=models.ManyToManyField(editable=False, through='management.OrderMaterial', to='management.material', verbose_name='Қолданылған материалдар'),
        ),
        migrations.AddField(
            model_name='order',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.service', verbose_name='Қызмет'),
        ),
        migrations.AddField(
            model_name='order',
            name='technician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.technician', verbose_name='Техник'),
        ),
    ]
