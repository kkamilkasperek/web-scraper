from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Article
from .serializers import ArticleSerializer

@api_view(['GET'])
def api_root(request):
    return Response({
        'articles': 'articles/',
        'article': 'articles/{id}/',
        'articles-filtered': 'articles/?domain={domain}'
    })

@api_view(['GET'])
def articles(request):
    source = request.GET.get('source', None)
    articles = Article.objects.filter(url__icontains=source) if source else Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def article(request, id):
    try:
        article = Article.objects.get(pk=id)
    except Article.DoesNotExist:
        return Response(
            {'error': f'Article with id {id} does not exist.'}, status=404)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)