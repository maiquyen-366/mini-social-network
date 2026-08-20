"""Tầng repository cơ sở: CRUD ORM tối thiểu dùng lại cho các app."""


class BaseRepository:
    model = None

    def get_by_id(self, object_id):
        return self.model.objects.filter(pk=object_id).first()

    def create(self, **data):
        return self.model.objects.create(**data)

    def update(self, instance, **data):
        if not data:
            return instance
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save(update_fields=list(data.keys()))
        return instance

    def delete(self, instance):
        instance.delete()
