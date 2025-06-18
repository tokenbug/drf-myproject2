from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    published_at = models.DateField()
    

    def __str__(self):
        return self.title
    
class BookImage(models.Model):
    # book = models.ForeignKey(Book, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='book_image', null=True, blank=True)
    book = models.ForeignKey(Book, related_name='images', on_delete=models.CASCADE)
    