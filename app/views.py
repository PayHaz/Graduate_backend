from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer


@api_view(['GET'])
def get_category_tree(request):
    parent_categories = Category.objects.filter(parent_id=None)
    return Response(CategorySerializer(parent_categories, many=True).data)
