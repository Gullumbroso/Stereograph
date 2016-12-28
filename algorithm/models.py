from django.db import models


class Characteristic(models.Model):
    value = models.CharField(max_length=200)
    opposite = models.CharField(max_length=200, default='', blank=True)
    group = models.CharField(max_length=200, default='', blank=True)

    class Meta:
        ordering = ['value']

    def __str__(self):
        return self.value


class Group(models.Model):
    value = models.CharField(max_length=200, unique=True)
    sub_groups = models.ForeignKey('self', related_name='parent', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['value']

    def __str__(self):
        return self.value


class Edge(models.Model):
    weight = models.FloatField(default=0)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    is_negative = models.BooleanField(default=False)

    def __str__(self):
        return self.source + ' to ' + self.destination
