from django.db import models

class Post(models.Model):
    by = models.CharField(max_length=200)
    descendants = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    text = models.TextField()
    time = models.DateTimeField() 
    title = models.CharField(max_length=300)
    type = models.CharField(max_length=50, choices=[('story', 'Story'), ('comment', 'Comment')])
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.title
    

