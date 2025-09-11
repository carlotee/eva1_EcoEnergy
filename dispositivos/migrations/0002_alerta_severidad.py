

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispositivos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerta',
            name='severidad',
            field=models.CharField(choices=[('grave', 'Grave'), ('alta', 'Alta'), ('mediana', 'Mediana')], default='mediana', max_length=10),
        ),
    ]
