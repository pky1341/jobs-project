# Generated by Django 4.1.7 on 2023-05-14 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_app', '0003_candidate_bio_candidate_country_candidate_education_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='annual_pay',
            field=models.BigIntegerField(blank=True, default=0, help_text='enter annual salary', null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='language',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='skill',
            field=models.TextField(blank=True, error_messages={'unique': 'A candidate with this skill already exists.'}, null=True),
        ),
    ]