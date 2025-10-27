from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
import os

# Import models that have File/ImageFields
from products.models import Inventory
from users.models import Profile, User, PortfolioImage
from orders.models import ArtisanUploadImage, OrderStatus
from users.models import ArtisanPortfolio

class Command(BaseCommand):
    help = 'Traverse MEDIA_ROOT and re-save model image fields so they upload to the current DEFAULT_FILE_STORAGE (e.g., Cloudinary).'

    def handle(self, *args, **options):
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        if not media_root:
            self.stdout.write(self.style.ERROR('MEDIA_ROOT is not set.'))
            return

        # Helper to resave an ImageField if local file exists
        def resave_field(instance, field_name):
            field = getattr(instance, field_name)
            if not field:
                return False
            local_path = os.path.join(media_root, field.name)
            if os.path.exists(local_path):
                with open(local_path, 'rb') as f:
                    django_file = File(f)
                    # Force overwrite by assigning a new File object with the same name
                    getattr(instance, field_name).save(os.path.basename(field.name), django_file, save=True)
                return True
            return False

        # Inventory images
        count = 0
        for obj in Inventory.objects.exclude(image='').iterator():
            if resave_field(obj, 'image'):
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Re-saved {count} Inventory images.'))

        # Profile images
        count = 0
        for obj in Profile.objects.exclude(image='').iterator():
            if resave_field(obj, 'image'):
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Re-saved {count} Profile images.'))

        # PortfolioImage
        count = 0
        for obj in PortfolioImage.objects.exclude(image='').iterator():
            if resave_field(obj, 'image'):
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Re-saved {count} PortfolioImage images.'))

        # ArtisanUploadImage
        count = 0
        for obj in ArtisanUploadImage.objects.exclude(image='').iterator():
            if resave_field(obj, 'image'):
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Re-saved {count} ArtisanUploadImage images.'))

        # OrderStatus images
        count = 0
        for obj in OrderStatus.objects.exclude(image='').iterator():
            if resave_field(obj, 'image'):
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Re-saved {count} OrderStatus images.'))

        self.stdout.write(self.style.SUCCESS('Done.'))