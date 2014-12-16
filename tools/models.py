from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name

class Tool(models.Model):
    function_name = models.CharField('Function Name', max_length=50)
    code = models.TextField()
    description = models.TextField()
    pub_date = models.DateField('Publication Date', default = datetime.now())
    author =  models.ForeignKey(User, editable=False)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.function_name

TYPE_OPTIONS = (
    (0, 'text'),
    (1, 'textarea'),
    )

class Parameter(models.Model):
    tool = models.ForeignKey(Tool)
    name = models.CharField(max_length=20)
    parameter_type = models.PositiveSmallIntegerField(choices = TYPE_OPTIONS)
    description = models.TextField()

    def __unicode__(self):
        return self.name


