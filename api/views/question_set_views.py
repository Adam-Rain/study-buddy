from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.question_set import QuestionSet
from ..serializers import QuestionSetSerializer, UserSerializer

# Create your views here.
class QuestionSets(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = QuestionSetSerializer
    def get(self, request):
        """Index request"""
        # Get all the Question Sets:
        question_sets = QuestionSet.objects.all()
        # Filter the Question Sets by owner, so you can only see your owned Question Sets
        # question_sets = QuestionSet.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = QuestionSetSerializer(question_sets, many=True).data
        return Response({ 'question_sets': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['question_set']['owner'] = request.user.id
        # Serialize/create mango
        question_set = QuestionSetSerializer(data=request.data['question_set'])
        # If the mango data is valid according to our serializer...
        if question_set.is_valid():
            # Save the created mango & send a response
            question_set.save()
            return Response({ 'question_set': question_set.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(question_set.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionSetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the mango to show
        question_set = get_object_or_404(QuestionSet, pk=pk)
        # Only want to show owned mangos?
        # if not request.user.id == question_set.owner.id:
        #     raise PermissionDenied('Unauthorized, you do not own this Question Set')

        # Run the data through the serializer so it's formatted
        data = QuestionSetSerializer(question_set).data
        return Response({ 'question_set': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate mango to delete
        question_set = get_object_or_404(QuestionSet, pk=pk)
        # Check the mango's owner agains the user making this request
        if not request.user.id == question_set.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this Question Set')
        # Only delete if the user owns the  mango
        question_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['mango'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['question_set'].get('owner', False):
            del request.data['question_set']['owner']

        # Locate Mango
        # get_object_or_404 returns a object representation of our Mango
        question_set = get_object_or_404(QuestionSet, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == question_set.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this Question Set')

        # Add owner to data object now that we know this user owns the resource
        request.data['question_set']['owner'] = request.user.id
        # Validate updates with serializer
        data = QuestionSetSerializer(question_set, data=request.data['question_set'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
