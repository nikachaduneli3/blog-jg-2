from django.core.management import BaseCommand
from posts.models import Post, Tag, Category

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--num', type=int)

    def handle(self, *args, **kwargs):
        num_post = kwargs.get('num', 0)
        category = Category.objects.first()
        tag = Tag.objects.first()
        content = 'test content '*10
        author_id = 1
        image = 'http://127.0.0.1:8000/media/posts/pngimg.com_-_circle_PNG71.png'

        for i in range(num_post):
            print(f'creating post: {i}')
            title = f'Test post {i}'
            post = Post(title=title, content=content, author_id=author_id, image=image, published=True)
            post.save()
            post.categories.add(category)
            post.tags.add(tag)

