from django.db import models
import datetime
from django.utils import timezone
from django.forms import ModelForm

class Question(models.Model):
    question_text = models.TextField('Question',max_length=200)
    answer_text = models.TextField('Answer',max_length=1000)
    #update_date is the last time the question was answered, and based on the counter_level, will determine the next time it should be answered
    update_date = models.DateTimeField('last answered')
    #tags needs to be a string because tags is really a list of varying length, and database needs to have a set number of columns (also keep in mind the max length of 200 and maybe allow 10 tags of length 20 each or check length each time you add a tag)
    tags = models.CharField(max_length=200, blank=True)
    #counter is from 0-5 inclusive, with 0 being the worst
    counter_level = models.IntegerField(default=0) #0-5
    periods = [1,5,13,31,75,200]
    skip = models.BooleanField(default=False)
    def is_new(self):
        """
        Returns True if the question is new and hasn't been reviewed yet
        """
        return True if self.counter_level == 0 else False

    def is_skipped(self):
        return self.skip

    #check if question will be ready to review soon:
    #def ready_soon(self):

    def days_left(self):
        """
        Returns the number of days remaining until the next review
        """
        SECONDS_PER_DAY = 86400
        #datetime.timedelta stores internally only days,seconds, microseconds
        seconds_since = (timezone.now() - self.update_date).total_seconds()
        days_since = seconds_since/SECONDS_PER_DAY
        days_left = self.periods[self.counter_level] - days_since
        return days_left

    def review_percent(self):
        """
        Returns the percentage of time until the next review that has passed
        """
        current_period = self.periods[self.counter_level]
        review_percent = (current_period-self.days_left())/current_period
        return review_percent

    def is_soon(self):
        num_days = 2
        days_left = self.days_left()
        return True if 0 < days_left < 2 else False

    def is_overdue(self):
        review_percent = self.review_percent()
        return True if review_percent >= 2 else False

    def update_counter(self):
        """
        This function is used when the user answers a question to update the counter based on the update_date and counter_level.
        """
        review_percent = self.review_percent()
        #don't reset counter for now
        #if review_percent >= 3:
        #    self.counter_level = 0 #reset counter if 3 times as long to review
        if review_percent >= 2:
            pass #keep counter the same if taking 2 times as long to review
        elif self.counter_level < len(self.periods)-1: 
            self.counter_level += 1 #increase counter_level
        self.update_date = timezone.now()

    def is_ready(self):
        """
        Returns true if Question is ready to be reviewed, and false otherwise.
        """
        days_left = self.days_left()
        if days_left <= 0:
            return True
        return False

    def __str__(self):
        return self.question_text

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'answer_text', 'tags']

