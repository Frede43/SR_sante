from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, Comment
from .forms import QuestionForm, CommentForm


# View to list all questions
class QuestionListView(ListView):
    model = Question
    template_name = 'forums/question_list.html'
    context_object_name = 'questions'

# View to display question details and comments
class QuestionDetailView(DetailView):
    model = Question
    template_name = 'forums/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(question=self.get_object(), parent_comment__isnull=True)
        context['form'] = CommentForm()
        return context

# View to create a new question
class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'forums/question_form.html'
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# View to create a comment or reply to a comment
# View to create a comment or reply to a comment
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'forums/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        question_id = self.kwargs['pk']
        parent_comment_id = self.kwargs.get('parent_id')

        # Link the comment to the question or parent comment
        form.instance.question = get_object_or_404(Question, pk=question_id)
        if parent_comment_id:
            form.instance.parent_comment = get_object_or_404(Comment, pk=parent_comment_id)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.kwargs['pk']})


