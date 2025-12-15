from django import forms
from recipes.models import Comment

# Form for creating a new comment on a recipe
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Share your thoughts…",
            }),
        }

