from django.db import models
from django.contrib.auth import get_user_model

# Create question set model
class QuestionSet(models.Model):
  topic = models.CharField(max_length=100)
  owner = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE
  )

  def __str__(self):
    return f"This set is about {self.topic} and is owned by {self.owner}"

  def as_dict(self):
    return {
    'id': self.id,
    'topic': self.topic
    }
