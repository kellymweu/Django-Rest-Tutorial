from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

#Serialization 2 imports
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

#Deserailization imports
import io

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     title = serializers.CharField(required = False, allow_blank = True, max_length = 100)
#     code = serializers.CharField(style={'base_template' : 'textarea.html'})
#     linenos = serializers.BooleanField(required = False)
#     language = serializers.ChoiceField(choices = LANGUAGE_CHOICES, default = 'python')
#     style = serializers.ChoiceField(choices = STYLE_CHOICES, default = 'friendly')

#     def create(self, validated_data):
#         # Create and return a new 'Snippet' instance, given the validated data

#         return Snippet.objects.create(**validated_data)
#     def update(sel, instance, validated_data):
#         # Update and return an existing 'Snippet' instance, given the validated data

#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id','highlight','owner', 'title', 'code', 'linenos', 'language', 'style']
        
#Adding endpoints for User Models
class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        field = ['url', 'id', 'username', 'snippets']
   
#defining the snippet save
snippet = Snippet(code = 'foo = "bar"\n')
snippet.save()

snippet = Snippet(code='print("hello world")\n')
snippet.save()

#SERIALIZE one of the instance
serializer = SnippetSerializer(snippet)
serializer.data
# {'id': 2, 'title': '', 'code': 'print("hello world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}

content = JSONRenderer().render(serializer.data)
content
# b'{"id": 2, "title": "", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'


# DESERIALIZATION
#parse stream into native datatypes
stream = io.BytesIO(content)
data = JSONParser().parse(stream)
#Restore native data types into a fully populated object instance
serializer = SnippetSerializer(data=data) 
serializer.is_valid()
#True
serializer.validated_data
# OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
serializer.save()
#<Snippet: Snippet object>

#SERIALIZE queryset
serializer = SnippetSerializer(Snippet.objects.all(), many=True)


