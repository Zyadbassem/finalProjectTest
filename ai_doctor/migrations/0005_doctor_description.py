# Generated by Django 5.0.6 on 2024-09-12 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_doctor', '0004_doctor_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='description',
            field=models.TextField(default='Dr. John is a skilled and compassionate dentist known for his patient-centered approach and expertise in comprehensive oral care.\n                With years of experience, Dr. John has built a reputation for delivering high-quality dental services,\n                including routine cleanings, advanced restorative work, and cosmetic dentistry.'),
        ),
    ]
