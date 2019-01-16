from django.db import models
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer_text = models.CharField(max_length=200)
    #update_date is the last time the question was answered, and based on the counter_level, will determine the next time it should be answered
    update_date = models.DateTimeField('last answered')
    #tags needs to be a string because tags is really a list of varying length, and database needs to have a set number of columns (also keep in mind the max length of 200 and maybe allow 10 tags of length 20 each or check length each time you add a tag)
    tags = models.CharField(max_length=200, blank=True)
    #counter is from 0-4 inclusive, with 0 being the worst
    counter_level = models.IntegerField(default=1) #0-4
    periods = [1,7,21,75,240]
    #check if question will be ready to review soon:
    #def ready_soon(self):
    def review_percent(self):
        """
        Returns the percentage of time that has passed until the next review date
        """
        SECONDS_PER_DAY = 86400
        #datetime.timedelta stores internally only days,seconds, microseconds
        seconds_since = (timezone.now() - self.update_date).total_seconds()
        days_since = seconds_since/SECONDS_PER_DAY
        review_percent = days_since/self.periods[self.counter_level]
        return review_percent

    def update_counter(self):
        """
        This function is used when the user answers a question to update the counter based on the update_date and counter_level.
        """
        review_percent = self.review_percent()
        if review_percent >= 3:
            self.counter_level = 0 #reset counter if 3 times as long to review
        elif review_percent >= 2:
            pass #keep counter the same if taking 2 times as long to review
        elif self.counter_level < len(self.periods)-1: 
            self.counter_level += 1 #increase counter_level
        self.update_date = timezone.now()

    def is_ready(self):
        """
        Returns true if Question is ready to be reviewed, and false otherwise.
        """
        period = self.periods[self.counter_level]
        next_review = self.update_date + datetime.timedelta(days=period)
        return timezone.now() >= next_review
    def __str__(self):
        return self.question_text

