# Generated by Django 5.0.7 on 2024-08-01 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_project_id_contributor_project_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contributor',
            old_name='project',
            new_name='project_id',
        ),
        migrations.RenameField(
            model_name='contributor',
            old_name='user',
            new_name='user_id',
        ),
        migrations.AlterUniqueTogether(
            name='contributor',
            unique_together={('user_id', 'project_id')},
        ),
    ]
