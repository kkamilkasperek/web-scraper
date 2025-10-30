from django.db import models

# Create your models here.

class Article(models.Model):
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=200, default='')
    html_content = models.TextField()
    text = models.TextField()
    date = models.DateTimeField(db_comment='Date of publication')

    def __str__(self):
        return self.url[:20] + ('...' if len(self.url) > 20 else '') + ' - ' + self.title