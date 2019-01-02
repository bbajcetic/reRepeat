from django.db import models
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer_text = models.CharField(max_length=200)
    #update_date is the last time the question was answered, and based on the counter_level, will determine the next time it should be answered
    update_date = models.DateTimeField('last answered')
    #tags needs to be a string because tags is really a list of varying length, and database needs to have a set number of columns (also keep in mind the max length of 200 and maybe allow 10 tags of length 20 each or check length each time you add a tag)
    tags = models.CharField(max_length=200)
    #counter is from 1-5 inclusive, with 1 being the worst
    counter_level = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

