from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE = (
        ('subscriber', 'Subscriber'),
        ('contributor', 'Contributor'),
        ('free', 'Free'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='free')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)


class Contributor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='contributors/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Edition(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    coverimage = models.ImageField(upload_to='editions/', blank=True, null=True)
    release_date = models.DateField()
    pdf_file = models.FileField(upload_to='edition_pdfs/', blank=True, null=True)  # PDF upload field


    def __str__(self):
        return self.name


# class Article(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     image = models.ImageField(upload_to='articles/', blank=True, null=True)
#     contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='articles')
#     edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name='articles')
#     publication_date = models.DateField()

#     def __str__(self):
#         return self.title


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()  # This will hold the short summary
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='articles')
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name='articles')
    publication_date = models.DateField()
    pdf_file = models.FileField(upload_to='article_pdfs/', blank=True, null=True)  # PDF upload field

    def __str__(self):
        return self.title

