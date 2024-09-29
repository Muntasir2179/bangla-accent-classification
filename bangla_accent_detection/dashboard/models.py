from django.db import models

# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField()


class AccentData(models.Model):
    predicted_accent = models.TextField(max_length=50)
    file_name = models.TextField(max_length=200)
    predicted_accent_confidence = models.FloatField(default=0.0)

    # each accents confidence
    barishal_conf = models.FloatField(default=0.0)
    bogura_conf = models.FloatField(default=0.0)
    chottogram_conf = models.FloatField(default=0.0)
    kurigram_conf = models.FloatField(default=0.0)
    madaripur_conf = models.FloatField(default=0.0)
    mymenshing_conf = models.FloatField(default=0.0)
    noakhali_conf = models.FloatField(default=0.0)
    pabna_conf = models.FloatField(default=0.0)
    puran_dhaka_conf = models.FloatField(default=0.0)
    rajshahi_conf = models.FloatField(default=0.0)
    shatkhira_conf = models.FloatField(default=0.0)
    sylhet_conf = models.FloatField(default=0.0)
    tahurgaon_conf = models.FloatField(default=0.0)

    # user feedback data
    user_prediction = models.TextField(max_length=50)

    # prediction indicator
    is_correct_prediction = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Accent Data'
    
    def __str__(self):
        return f'{self.file_name}'