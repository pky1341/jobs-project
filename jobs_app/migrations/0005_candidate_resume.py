# Generated by Django 4.1.7 on 2023-05-14 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_app', '0004_candidate_annual_pay_candidate_language_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='resume',
            field=models.FileField(blank=True, default=None, help_text='Upload your resume in PDF format.', null=True, upload_to='jobs_app/resume/Candidate'),
        ),
    ]
