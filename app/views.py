from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Article, Edition, Contributor, User
from .serializers import ArticleSerializer, EditionSerializer, ContributorSerializer, RegisterSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reportlab.pdfgen import canvas
from io import BytesIO
from rest_framework.decorators import action


from django.contrib.auth import authenticate, login


# class LoginView(APIView):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         if not username or not password:
#             return Response(
#                 {"error": "Username and password are required."}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)  # Logs the user into the session (if using session-based authentication)
#             return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
#         else:
#             return Response(
#                 {"error": "Invalid username or password."}, 
#                 status=status.HTTP_401_UNAUTHORIZED
#             )


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Username and password are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "refresh": str(refresh),
                "access": access_token
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid username or password."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type,
            },
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

# class EditionViewSet(viewsets.ModelViewSet):
#     queryset = Edition.objects.all()
#     serializer_class = EditionSerializer

# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         # Automatically associate the logged-in user as the contributor
#         serializer.save(contributor=self.request.user.contributor)



## Working
# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         # Automatically associate the logged-in user as the contributor
#         serializer.save(contributor=self.request.user.contributor)

#     @action(detail=True, methods=['get'])
#     def download(self, request, pk=None):
#         # Retrieve the article object
#         article = self.get_object()

#         # Generate PDF content
#         buffer = BytesIO()
#         pdf = canvas.Canvas(buffer)
#         pdf.drawString(100, 800, f"Title: {article.title}")
#         pdf.drawString(100, 780, f"Contributor: {article.contributor}")
#         pdf.drawString(100, 760, f"Publication Date: {article.publication_date}")
#         pdf.drawString(100, 740, "Content:")
#         pdf.drawString(100, 720, article.content[:1000])  # Truncate long content for demo purposes

#         pdf.save()
#         buffer.seek(0)

#         # Return the PDF file as a response
#         response = HttpResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="article_{article.id}.pdf"'
#         return response

# from reportlab.lib.pagesizes import letter
# from reportlab.lib import utils

# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(contributor=self.request.user.contributor)

#     @action(detail=True, methods=['get'])
#     def download(self, request, pk=None):
#         article = self.get_object()

#         # Prepare PDF
#         buffer = BytesIO()
#         pdf = canvas.Canvas(buffer, pagesize=letter)
#         width, height = letter  # Page dimensions
#         x_margin = 50  # Left margin
#         y_start = height - 50  # Start from top with some margin

#         # Write Title and Metadata
#         pdf.setFont("Helvetica-Bold", 16)
#         pdf.drawString(x_margin, y_start, f"Title: {article.title}")
#         y_start -= 20
#         pdf.setFont("Helvetica", 12)
#         pdf.drawString(x_margin, y_start, f"Contributor: {article.contributor}")
#         y_start -= 20
#         pdf.drawString(x_margin, y_start, f"Publication Date: {article.publication_date}")
#         y_start -= 40  # Space before content

#         # Wrap Content Text
#         content = article.content
#         text_object = pdf.beginText(x_margin, y_start)
#         text_object.setFont("Helvetica", 12)
#         text_object.setTextOrigin(x_margin, y_start)

#         max_width = width - (2 * x_margin)  # Text wrapping width
#         lines = self._wrap_text(content, max_width, pdf)

#         for line in lines:
#             if y_start < 50:  # Check if a new page is needed
#                 pdf.showPage()
#                 y_start = height - 50
#                 text_object = pdf.beginText(x_margin, y_start)
#                 text_object.setFont("Helvetica", 12)

#             text_object.textLine(line)
#             y_start -= 15

#         pdf.drawText(text_object)
#         pdf.save()
#         buffer.seek(0)

#         # Return PDF as Response
#         response = HttpResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="article_{article.id}.pdf"'
#         return response

#     def _wrap_text(self, text, max_width, pdf):
#         """
#         Helper method to wrap text to fit within a specific width.
#         """
#         from reportlab.pdfbase.pdfmetrics import stringWidth
#         words = text.split()
#         lines = []
#         current_line = []

#         for word in words:
#             current_line.append(word)
#             line_width = stringWidth(' '.join(current_line), pdf._fontname, pdf._fontsize)
#             if line_width > max_width:
#                 # Line too long, wrap
#                 current_line.pop()  # Remove last word
#                 lines.append(' '.join(current_line))
#                 current_line = [word]  # Start a new line with the word

#         if current_line:
#             lines.append(' '.join(current_line))

#         return lines


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically associate the logged-in user as the contributor
        serializer.save(contributor=self.request.user.contributor)

    
## Working
# class EditionViewSet(viewsets.ModelViewSet):
#     queryset = Edition.objects.all()
#     serializer_class = EditionSerializer

#     @action(detail=True, methods=['get'])
#     def download(self, request, pk=None):
#         edition = self.get_object()
#         articles = edition.articles.all()
        
#         # Generate PDF content
#         buffer = BytesIO()
#         pdf = canvas.Canvas(buffer)
#         y = 800
#         pdf.drawString(100, y, f"Edition: {edition.id}")
#         y -= 20
        
#         for article in articles:
#             pdf.drawString(100, y, f"Title: {article.title}")
#             y -= 20
#             pdf.drawString(100, y, f"Contributor: {article.contributor}")
#             y -= 20
#             pdf.drawString(100, y, f"Publication Date: {article.publication_date}")
#             y -= 20
#             pdf.drawString(100, y, f"Content Preview: {article.content[:100]}")
#             y -= 40  # Leave space between articles

#             if y < 100:  # Start a new page if there's no space
#                 pdf.showPage()
#                 y = 800

#         pdf.save()
#         buffer.seek(0)

#         # Return the PDF file as a response
#         response = HttpResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="edition_{edition.id}.pdf"'
#         return response



import os
from zipfile import ZipFile
class EditionViewSet(viewsets.ModelViewSet):
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer

    @action(detail=True, methods=['get'])
    def download_articles(self, request, pk=None):
        # Get the edition and its related articles
        edition = self.get_object()
        articles = edition.articles.all()  # Related name for the foreign key

        # Create a zip file in memory
        buffer = BytesIO()
        with ZipFile(buffer, 'w') as zip_file:
            for article in articles:
                if article.pdf_file:
                    # Add each article's PDF file to the zip
                    file_path = article.pdf_file.path
                    file_name = os.path.basename(file_path)
                    zip_file.write(file_path, f"{edition.name}/{file_name}")

        buffer.seek(0)

        # Return the zip file as a downloadable response
        response = HttpResponse(buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="edition_{edition.id}_articles.zip"'
        return response

    @action(detail=True, methods=['get'])
    def articles(self, request, pk=None):
        """
        Retrieve all articles related to a specific edition.
        """
        edition = self.get_object()
        articles = edition.articles.all()  # Assuming the related name is `articles`
        # serializer = ArticleSerializer(articles, many=True)
        serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)
        # return Response(serializer.data)