from rest_framework import serializers

from ..models import Subject, Course, Module, Content


class SubjectSerializer(serializers.ModelSerializer):
    """Serialization of subject objects"""

    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    """Serialization of module objects"""

    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    """Serialization of Course objects"""

    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules']


class ItemRelatedField(serializers.RelatedField):
    """Serialization of every content model objects"""

    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    """Serialization of the content objects"""
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """Serialization the module objects"""
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentSerializer(serializers.ModelSerializer):
    """Serialization of the full course content"""
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules']
