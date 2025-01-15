from django.db import models
from datetime import datetime
# Create your models here.

class Course(models.Model):
    LEVELS = [
        ('All Levels', 'All Levels'),
        ('Intermediate Level', 'Intermediate level'),
        ('Beginner Level', 'Beginner level'),
        ('Expert Level', 'Expert level')
    ]

    SUBJECT = [
        ('Business Finance', 'Business Finance'),
        ('Graphic Design', 'Graphic Design'),
        ('Musical Instruments', 'Musical Instruments'),
        ('Web Development', 'Web Development')
    ]

    course_id = models.IntegerField(blank=True, null=True)
    course_title = models.CharField(max_length=1000, blank=True, null=True)
    url = models.URLField(null=True, blank=True, max_length=1000)
    is_paid = models.CharField(max_length=1000, blank=True, null=True)
    price = models.CharField(max_length=1000, blank=True, null=True)
    subscribers = models.IntegerField(blank=True, null=True)
    num_lectures = models.IntegerField(blank=True, null=True)
    reviews = models.IntegerField(blank=True, null=True)
    level = models.CharField(max_length=100, blank=True, null=True, choices=LEVELS)
    content_duration = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=500, blank=True, null=True, choices=SUBJECT)
    published_timestamp = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def published_on(self):
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        datetime_object = datetime.strptime(self.published_timestamp, date_format)
        return datetime_object

    def __str__(self):
        return self.course_title


