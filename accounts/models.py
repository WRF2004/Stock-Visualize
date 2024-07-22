from django.db import models
from django.contrib.auth.models import User
import os

def user_directory_path(instance, filename):
    # 文件将上传到 MEDIA_ROOT/uploads/user_<id>/<filename>
    return f'uploads/user_{instance.user.id}/{filename}'

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    upload_time = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=255, blank=True)  

    class Meta:
        ordering = ['-upload_time']  

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        
        super().delete(*args, **kwargs)