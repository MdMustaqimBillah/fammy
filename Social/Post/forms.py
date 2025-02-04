from django import forms
from .models import Comment


# the below code fragment can be found in:


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.TextInput(attrs={'placeholder': 'Place your opinion'})
        }