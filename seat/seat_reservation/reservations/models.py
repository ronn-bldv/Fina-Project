from django.db import models
from django.contrib.auth.models import User
import uuid

# Base Model to be inherited by other models
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

# Venue Model
class Venue(models.Model):
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    seats_per_row = models.PositiveIntegerField()

    def __str__(self):
        return self.name


# Seat Model for Reservation System (renamed)
class Seat(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="seats")
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"Row {self.row}, Seat {self.number} in {self.venue.name}"


# Reservation Model
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} reserved {self.seat}"


# Movie Category Model
class MovieCategory(BaseModel):
    category_name = models.CharField(max_length=100)

# Movie Model
class Movie(BaseModel):
    category = models.ForeignKey(MovieCategory, on_delete=models.CASCADE, related_name="movies")
    movie_name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    images = models.ImageField(null=True, blank=True, upload_to="images/")
    available_dates = models.ManyToManyField('MovieDateTime', related_name="movies")

# Movie DateTime Model
class MovieDateTime(BaseModel):
    date = models.DateField()
    time = models.TimeField()

# Movie Seat Model (renamed from Seat to MovieSeat)
class MovieSeat(BaseModel):
    movie_datetime = models.ForeignKey(MovieDateTime, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10)
    is_taken = models.BooleanField(default=False)

# Cart Model
class Cart(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="carts")
    is_paid = models.BooleanField(default=False)

# CartItems Model
class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_datetime = models.ForeignKey(MovieDateTime, on_delete=models.CASCADE)  # ForeignKey to MovieDateTime
    seat = models.ForeignKey(MovieSeat, null=True, blank=True, on_delete=models.CASCADE)  # Changed to MovieSeat
    seat_numbers = models.CharField(max_length=255, null=True, blank=True)  # To store comma-separated seat numbers
