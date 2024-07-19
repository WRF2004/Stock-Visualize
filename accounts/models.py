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

    name = models.CharField(max_length=255, blank=True)  # 文件名

    class Meta:
        ordering = ['-upload_time']  # 按上传时间降序排序

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        # 首先删除文件系统中的文件
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        # 然后删除数据库中的记录
        super().delete(*args, **kwargs)

# class StockData(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
#     stock_code = models.CharField(max_length=20)
#     date = models.DateField()
#     open_price = models.DecimalField(max_digits=10, decimal_places=2)
#     close_price = models.DecimalField(max_digits=10, decimal_places=2)
#     high_price = models.DecimalField(max_digits=10, decimal_places=2)
#     low_price = models.DecimalField(max_digits=10, decimal_places=2)
#     volume = models.BigIntegerField()
#     change = models.DecimalField(max_digits=5, decimal_places=2)
#     amplitude = models.DecimalField(max_digits=5, decimal_places=2)
#     turnover = models.DecimalField(max_digits=5, decimal_places=2)

#     def __str__(self):
#         return f"{self.stock_code} - {self.date}"


