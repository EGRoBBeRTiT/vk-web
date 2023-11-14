from django.core.management.base import BaseCommand
from datetime import datetime
from random import randint
from app import models


class Command(BaseCommand):
    help = 'Command manager to fill database'

    def handle(self, *args, **options):
        ratio = options['ratio']
        users_for_create = [
            models.Profile(
                username=f'user{i}',
                password=f'user{i}',
                first_name=f'name of user{i}',
                last_name=f'surname of user{i}',
                email=f'user{i}@google.com',
                is_staff=False,
                is_active=True,
                avatar=f'{randint(1, 20)}.jpg',
                nickname=f'nickname{i}'
            ) for i in range(ratio)
        ]
        models.Profile.objects.bulk_create(users_for_create)

        tags_for_create = [
            models.Tag(
                tag=f'tag {i}',
            ) for i in range(ratio)
        ]
        models.Tag.objects.bulk_create(tags_for_create)

        likes_to_create = [
            models.Like(
                amount_of_likes=randint(1, ratio)
            ) for i in range(ratio * 110)
        ]
        models.Like.objects.bulk_create(likes_to_create)

        like_profile = []
        likes = models.Like.objects.all()
        for i in range(ratio * 110):
            current_likes = likes[i].amount_of_likes
            for j in range(current_likes):
                like_profile.append(
                    models.Like.voted_users.through(
                        like_id=i + 1,
                        profile_id=j + 1
                    )
                )
        models.Like.voted_users.through.objects.bulk_create(like_profile)

        users = models.Profile.objects.all()
        tags = models.Tag.objects.all()
        likes = models.Like.objects.all()
        questions_for_create = [
            models.Question(
                title=f'title of question {i}',
                text=f'text of question {i}',
                profile_id=users[randint(0, ratio - 1)],
                likes=likes[i]
            ) for i in range(ratio * 10)
        ]
        models.Question.objects.bulk_create(questions_for_create)

        question_tag = []
        for i in range(ratio * 10):
            amount_of_tags = randint(1, ratio)
            for j in range(amount_of_tags):
                question_tag.append(
                    models.Question.tags.through(
                        question_id=i + 1,
                        tag_id=j + 1
                    )
                )
        models.Question.tags.through.objects.bulk_create(question_tag)

        questions = models.Question.objects.all()
        answers_for_create = []
        for i in range(ratio * 100):
            question_id = randint(0, ratio * 10 - 1)
            answers_for_create.append(
                models.Answer(
                    question_id=questions[ratio * 10 - 1 - question_id],
                    text=f'text of answer {i}',
                    profile_id=users[randint(0, ratio - 1)],
                    is_correct=True if randint(0, 1) else False,
                    likes=likes[i + ratio * 10]
                )
            )
            questions.filter(id=question_id + 1).update(amount_of_answers=questions[ratio * 10 - 1 - question_id].amount_of_answers + 1)
        models.Answer.objects.bulk_create(answers_for_create)

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)
