from django.db import models
from django.contrib.auth.models import User

class UploadImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="posted_img")
    timestamp = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if self.user == "":
    #         self.user = request.user
    #     super().save(*args, **kwargs)

    def __str__(self):
        return "User: " + str(self.user) + " | Image: " + str(self.image)
    

class UploadVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    video = models.FileField(upload_to="posted_video")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User: " + str(self.user) + " | Video: " + str(self.video)

class Follow(models.Model):
    which_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="which_user")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.following_user) + " connected to: " + str(self.which_user)
