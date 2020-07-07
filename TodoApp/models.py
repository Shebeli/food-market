from django.db import models
from django.shortcuts import reverse

class ToDoApp(models.Model):
    category = models.CharField(max_length=30)
    description = models.TextField()
    date = models.DateTimeField()


    def __str__(self):
        return self.category


    def delete_url(self):
        return reverse("todo-delete", kwargs={"id": self.pk})

    #def get_absolute_url(self):
        #return reverse("model_detail", kwargs={"pk": self.pk})
    
