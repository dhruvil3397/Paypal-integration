from django.db import models

# Create your models here.
class Blogpost(models.Model):   
    post_id = models.AutoField(primary_key=True)   
    title = models.CharField(max_length=50)
    heading1 = models.CharField(max_length=500)
    content1 = models.CharField(max_length=5000)
    heading2 = models.CharField(max_length=500)
    content2 = models.CharField(max_length=5000)
    heading3= models.CharField(max_length=500)
    content3 = models.CharField(max_length=5000)
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to = 'blog/images')
    


    def __str__(self) -> str:
        return self.title
