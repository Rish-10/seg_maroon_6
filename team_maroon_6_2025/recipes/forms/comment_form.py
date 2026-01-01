from django import forms
from recipes.models import Comment

class CommentForm(forms.ModelForm):
    """
    Form for creating a new comment on a recipe.

    This form collects the body of the comment (the message contents)
    the user wishes to make.
    """

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

