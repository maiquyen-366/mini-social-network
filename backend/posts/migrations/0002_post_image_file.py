"""Migration thêm file ảnh bài đăng local, giữ nguyên image_url cũ."""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("posts", "0001_initial")]
    operations = [
        migrations.AddField(
            model_name="post",
            name="image_file",
            field=models.FileField(blank=True, null=True, upload_to="posts/"),
        ),
    ]
