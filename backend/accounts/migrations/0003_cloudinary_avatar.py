"""Migration chuyển avatar local sang secure URL và public_id Cloudinary."""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("accounts", "0002_user_avatar_file")]
    operations = [
        migrations.RemoveField(model_name="user", name="avatar_file"),
        migrations.AddField(
            model_name="user",
            name="avatar_public_id",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
