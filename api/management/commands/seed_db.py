from django.core.management.base import BaseCommand
from faker import Faker
from api.models import Post
import random
from django.utils import timezone 

class Command(BaseCommand):
    help = "Seeds the database with fake posts."

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=1000, help='Number of posts to create')
        parser.add_argument('--depth', type=int, default=3, help='Maximum depth of comment nesting')

    def handle(self, *args, **options):
        count = options['count']
        depth = options['depth']
        faker = Faker()

        stories = [
            Post(
                by=faker.name(),
                descendants=0,  
                score=random.randint(1, 100),
                text=faker.text(),
                time=timezone.make_aware(faker.date_time_this_decade()),
                title=faker.sentence(),
                type='story'
            ) for _ in range(count // 2)  
        ]
        Post.objects.bulk_create(stories)
        print(f'Added {len(stories)} stories.')

        story_ids = list(Post.objects.filter(type='story').values_list('id', flat=True))

        def create_comments(parent_id, current_depth=1):
            if current_depth > depth:
                return
            num_comments = random.randint(1, 3)  
            comments = [
                Post(
                    by=faker.name(),
                    score=random.randint(1, 100),
                    text=faker.text(),
                    time=timezone.make_aware(faker.date_time_this_decade()),
                    title=faker.sentence(),
                    type='comment',
                    parent_id=parent_id
                ) for _ in range(num_comments)
            ]
            Post.objects.bulk_create(comments)
            for comment in comments:
                create_comments(comment.id, current_depth + 1)

        for story_id in story_ids:
            create_comments(story_id)

        for post in Post.objects.filter(type='story'):
            post.descendants = post.children.count()
            post.save()

