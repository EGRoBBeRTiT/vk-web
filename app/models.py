from django.contrib.auth.models import AbstractUser
from django.db import models


class ProfileManager(models.Manager):
    def get_user_by_username(self, username):
        return self.filter(username=username)

    def get_best_members(self):
        return self.filter(id__lt=6)


class Profile(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/')
    nickname = models.CharField(max_length=20)

    objects = ProfileManager()


class Like(models.Model):
    amount_of_likes = models.IntegerField(default=0)
    voted_users = models.ManyToManyField(Profile)


class TagManager(models.Manager):
    def get_popular_tags(self):
        return self.filter(id__lt=9)


class Tag(models.Model):
    tag = models.CharField(max_length=30)

    objects = TagManager()

    def __str__(self):
        return self.tag


class QuestionManager(models.Manager):
    def get_hot_questions(self):
        return self.order_by('-likes__amount_of_likes')

    def get_new_questions(self):
        return self.order_by('-date_of_creation')

    def get_questions_by_tag(self, tag):
        return self.filter(tags__tag=tag)


class Question(models.Model):
    title = models.CharField(max_length=90)
    text = models.TextField(max_length=512)
    profile_id = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    likes = models.OneToOneField(Like, on_delete=models.CASCADE)
    amount_of_answers = models.IntegerField(default=0)

    objects = QuestionManager()

    class Meta:
        ordering = ['-id']


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=512)
    profile_id = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    likes = models.OneToOneField(Like, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

