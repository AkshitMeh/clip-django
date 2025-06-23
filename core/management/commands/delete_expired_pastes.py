from django.core.management.base import BaseCommand
from core.models import Paste
from django.utils import timezone

class Command(BaseCommand):
    help = 'Delete expired pastes from the database and remove their files.'

    def handle(self, *args, **options):
        now = timezone.now()
        expired_pastes = Paste.objects.filter(expires_at__isnull=False, expires_at__lt=now)
        count = 0
        for paste in expired_pastes:
            if paste.file_content:
                paste.file_content.delete(save=False)
            paste.delete()
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} expired pastes.'))
