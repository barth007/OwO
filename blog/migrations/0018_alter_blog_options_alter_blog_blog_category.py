# Generated by Django 4.2.8 on 2023-12-22 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_remove_blog_like_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-created_at'], 'verbose_name': 'Blog', 'verbose_name_plural': 'Blogs'},
        ),
        migrations.AlterField(
            model_name='blog',
            name='blog_category',
            field=models.CharField(choices=[('finance', 'Finance'), ('health', 'Health'), ('web_Design', 'Web Design'), ('technology', 'Technology'), ('banking_services', 'Banking Services'), ('investment', 'Investment'), ('financial_markets', 'Financial Markets'), ('credit_cards', 'Credit Cards'), ('mortgages', 'Mortgages'), ('online_banking', 'Online Banking'), ('personal_finance', 'Personal Finance'), ('business_finance', 'Business Finance')], default='draft', help_text='Select the category of your blog', max_length=20),
        ),
    ]
