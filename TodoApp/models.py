from django.db import models

class ToDoApp(models.Model):
    category = models.CharField(max_length=30)
    description = models.TextField()
    date = models.DateTimeField()


    def __str__(self):
        return self.category
