from django.urls import path
from .views import QuestionListView, QuestionDetailView, QuestionCreateView, CommentCreateView

urlpatterns = [
    path('', QuestionListView.as_view(), name='question_list'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question/new/', QuestionCreateView.as_view(), name='question_create'),
    path('question/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('question/<int:pk>/comment/<int:parent_id>/', CommentCreateView.as_view(), name='comment_reply'),
]


