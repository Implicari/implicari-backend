# Generated by Django 4.1.3 on 2022-11-17 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classrooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('files', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.FileField(upload_to=''), size=None)),
                ('is_sent', models.BooleanField(default=False)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='classrooms.classroom')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
