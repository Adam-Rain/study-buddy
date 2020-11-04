from django.db import models
from django.contrib.auth import get_user_model

# Create question model
class Question(models.Model):
  question = models.CharField(max_length=500)
  answer = models.CharField(max_length=500)
  question_set = models.ForeignKey(
    'QuestionSet',
    related_name='questions',
    on_delete=models.CASCADE
  )

  def __str__(self):
    return f"Here is the question: {self.question}. Here is the answer: {self.answer}."

  def as_dict(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer
    }
