from django.db import models
import random

class Paste(models.Model):
    code = models.CharField(max_length=4, unique=True)
    content_type = models.CharField(max_length=10)  # 'text' or 'file'
    text_content = models.TextField(blank=True, null=True)
    file_content = models.FileField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_code():
        while True:
            code = f"{random.randint(0, 9999):04d}"
            if not Paste.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return self.code