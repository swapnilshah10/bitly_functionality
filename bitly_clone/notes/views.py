from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Note
from .serializers import  NoteSerializer



from django.db import IntegrityError

@api_view(['POST'])
def create_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Create the user
        user = CustomUser.objects.create(username=username, password=password)
        return Response({'message': 'User created successfully', 'user_id': user.id}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def save_note(request):
    username = request.data.get('username')
    password = request.data.get('password')
    title = request.data.get('title')
    content = request.data.get('content')

    try:
        user = CustomUser.objects.get(username=username, password=password)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    note = Note.objects.create(user=user, title=title, content=content)
    return Response({'message': 'Note saved successfully', 'note_id': note.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def retrieve_notes(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = CustomUser.objects.get(username=username, password=password)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    notes = Note.objects.filter(user=user)
    serializer = NoteSerializer(notes, many=True)
    return Response({'notes': serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def edit_note(request, note_id):
    username = request.data.get('username')
    password = request.data.get('password')
    title = request.data.get('title')
    content = request.data.get('content')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Authenticate the user
        user = CustomUser.objects.get(username=username, password=password)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Fetch the note
        note = Note.objects.get(id=note_id, user=user)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

    # Update the note
    if title:
        note.title = title
    if content:
        note.content = content
    note.save()

    return Response({'message': 'Note updated successfully'}, status=status.HTTP_200_OK)

