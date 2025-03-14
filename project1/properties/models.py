from django.db import models

class Property(models.Model):
    PROPERTY_TYPES = [
        ('rent', 'Rent'),
        ('buy', 'Buy')
    ]

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    image = models.ImageField(upload_to='property_images/', default='property_images/default.jpg')
    rating = models.FloatField(default=0.0)
    reviews_count = models.IntegerField(default=0)
    reviews = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def update_rating(self, new_rating):
        total_rating = (self.rating * self.reviews_count) + new_rating
        self.reviews_count += 1
        self.rating = total_rating / self.reviews_count
        self.save()
