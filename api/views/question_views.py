from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.question import Question
from ..serializers import QuestionSerializer, UserSerializer

# Create your views here.
class Question(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = QuestionSetSerializer
    def get(self, request):
        """Index request"""
        # Get all the Questions:
        questions = Question.objects.all()
        # Filter the Question Sets by owner, so you can only see your owned Question Sets
        # question_sets = QuestionSet.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = QuestionSerializer(questions, many=True).data
        return Response({ 'questions': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['question']['owner'] = request.user.id
        # Serialize/create question
        question = QuestionSerializer(data=request.data['question'])
        # If the question data is valid according to our serializer...
        if question.is_valid():
            # Save the created question & send a response
            question.save()
            return Response({ 'question': question.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(question.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the question to show
        question = get_object_or_404(Question, pk=pk)
        # Only want to show owned mangos?
        # if not request.user.id == question_set.owner.id:
        #     raise PermissionDenied('Unauthorized, you do not own this Question Set')

        # Run the data through the serializer so it's formatted
        data = QuestionSerializer(question).data
        return Response({ 'question': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate question to delete
        question = get_object_or_404(Question, pk=pk)
        # Check the question's owner agains the user making this request
        if not request.user.id == question.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this Question')
        # Only delete if the user owns the  question
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['question'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['question'].get('owner', False):
            del request.data['question']['owner']

        # Locate question
        # get_object_or_404 returns a object representation of our question
        question = get_object_or_404(Question, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == question.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this Question')

        # Add owner to data object now that we know this user owns the resource
        request.data['question']['owner'] = request.user.id
        # Validate updates with serializer
        data = QuestionSerializer(question, data=request.data['question'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
