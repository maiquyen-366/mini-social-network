"""Tầng Serializer/DTO: format User và validate cập nhật hồ sơ."""

from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "avatar_url", "bio"]
        read_only_fields = ["id", "username"]

    def get_avatar_url(self, obj):
        url = obj.avatar_url or ""
        request = self.context.get("request")
        return request.build_absolute_uri(url) if request and url.startswith("/") else url


class ProfileUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    avatar_file = serializers.FileField(required=False, allow_null=True, write_only=True)
    remove_avatar = serializers.BooleanField(required=False, default=False, write_only=True)
    bio = serializers.CharField(required=False, allow_blank=True, max_length=500)

    def validate_avatar_file(self, value):
        from core.file_validation import validate_image_file

        return validate_image_file(value)

    def validate(self, attrs):
        if attrs.get("avatar_file") and attrs.get("remove_avatar"):
            raise serializers.ValidationError("Chỉ chọn đổi ảnh hoặc xóa ảnh tại một thời điểm.")
        return attrs
