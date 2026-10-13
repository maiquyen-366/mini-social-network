"""Migration dữ liệu: giữ các đoạn chat cũ bằng cách xem hai người đã chat là bạn bè."""

from django.db import migrations


def make_existing_chat_participants_friends(apps, schema_editor):
    Friendship = apps.get_model("accounts", "Friendship")
    Conversation = apps.get_model("chat", "Conversation")

    for conversation in Conversation.objects.prefetch_related("participants").all():
        participant_ids = list(conversation.participants.values_list("id", flat=True))
        if len(participant_ids) != 2:
            continue
        requester_id, addressee_id = sorted(participant_ids)
        Friendship.objects.get_or_create(
            requester_id=requester_id,
            addressee_id=addressee_id,
            defaults={"status": "accepted"},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_friendship"),
        ("chat", "0002_message_read_at"),
    ]

    operations = [
        migrations.RunPython(make_existing_chat_participants_friends, migrations.RunPython.noop),
    ]
