from django.contrib.auth.models import User
from django.db import models


class Piano(models.Model):
    brand = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    size = models.IntegerField(blank=True)
    imageUrl = models.URLField(max_length=200, blank=True)
    owner = models.ForeignKey(User, 
                              on_delete=models.CASCADE, 
                              related_name="pianos")

    def __str__(self):
        return f"${self.brand}: ${self.price}"

 
class Vote(models.Model):
    voter = models.ForeignKey(User, 
                              on_delete=models.CASCADE, 
                              related_name="user_votes", 
                              null=True)
    item = models.ForeignKey(Piano, 
                             on_delete=models.CASCADE, 
                             related_name="piano_votes", 
                             null=True)
    vote_type = models.SmallIntegerField(choices=[(1, "Upvote"), (-1, "Downvote")], 
                                         null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voter.username} voted {self.vote_type} for {self.item.brand}"


class Comment(models.Model):
    text = models.TextField()
    comment = models.ForeignKey(Piano, 
                                on_delete=models.CASCADE, 
                                related_name="piano_comments")
    commenter = models.ForeignKey(User, 
                                  on_delete=models.CASCADE, 
                                  related_name="user_comments")

    def __str__(self):
        return f"${self.text} by ${self.commenter.username}"
    









