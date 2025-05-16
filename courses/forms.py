from django import forms

class QuestionForm(forms.Form):
    question = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Type your question here...',
            'rows': 4,
            'class': 'form-control',
        }),
        label=''
    )
