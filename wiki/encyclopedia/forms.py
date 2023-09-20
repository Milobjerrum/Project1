from django import forms

from django.core.exceptions import ValidationError

from . import util

# New page Django form 
class NewPageForm(forms.Form):
    # Fields, for the titel and the content
    title = forms.CharField(
        label="Title")
    content = forms.CharField(
        label="", 
        widget=forms.Textarea(attrs={
            "placeholder": "Content"
        })
        )

    # Ensure valid title
    def clean_title(self):
        title = self.cleaned_data.get("title")
        # Check if the title alredy exsists
        if title in util.list_entries():
            raise forms.ValidationError(
                "There is alredy an entry with this title"
                )
        else:
            return title


class EditPageForm(forms.Form):
    titel = forms.CharField(widget=forms.HiddenInput())
    content = forms.CharField(
        label="",
        widget=forms.Textarea( 
        )
    )