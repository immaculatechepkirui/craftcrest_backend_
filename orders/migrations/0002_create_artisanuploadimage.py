from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtisanUploadImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='order_images/')),
                ('artisan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_images', to=settings.AUTH_USER_MODEL)),
                ('custom_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artisan_uploads', to='orders.CustomDesignRequest')),
            ],
        ),
    ]