from rest_framework import serializers
from .models import Snippet
from django.contrib.auth.models import User

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta: 
        model = Snippet
        fields = [ 'url', 'id', 'title', 'code', 'linenos', 
                'language', 'style', 'owner', 'highlight']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedIdentityField(many=True, view_name="snippet-detail", read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']


# class SnippetSerializer(serializers.Serializer):
#     '''The fields that get serialized / deserialized'''
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#     # create and update method define how instances are created and modified
#     # when calling serializer.save()
#     def create(self, validated_data):
#         '''Create and return a new Snippet instance with the validated_data'''
#         return Snippet.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

# difference ModelSerializer compare to Serializer:
# automatically determined set of fields
# simple default implementations for the create() and update()