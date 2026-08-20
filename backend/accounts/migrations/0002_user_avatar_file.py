"""Migration thêm file avatar local, giữ nguyên avatar_url cũ."""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("accounts", "0001_initial")]
    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar_file",
            field=models.FileField(blank=True, null=True, upload_to="avatars/"),
        ),
    ]
