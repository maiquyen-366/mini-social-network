"""Migration chuyển ảnh bài đăng local sang secure URL và public_id Cloudinary."""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("posts", "0002_post_image_file")]
    operations = [
        migrations.RemoveField(model_name="post", name="image_file"),
        migrations.AddField(
            model_name="post",
            name="image_public_id",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
