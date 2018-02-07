from django.db import models


class Metadata(models.Model):
    # Id = models.IntegerField()
    Name = models.TextField()
    Path = models.TextField()
    Extension = models.TextField()
    Size = models.TextField()
    Date = models.DateTimeField()


def __str__(self):
    return self.Name + '' + self.Path + '' + self.Extension + '' + self.Size + '' + self.Date
