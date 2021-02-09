from django.db import models

# Create your models here.

class Motion(models.Model):
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    camera_index = models.PositiveIntegerField(null=True,blank=True)

    class Meta:
        verbose_name = "Motion"
        verbose_name_plural = "Motions"

    def __str__(self):
        return str(self.start_time)

    def get_absolute_url(self):
        return reverse("Motion_detail", kwargs={"pk": self.pk})


