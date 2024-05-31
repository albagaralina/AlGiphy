from django import forms

class EmailForm(forms.Form):
    recipient = forms.EmailField(label="Recipient's Email Address")
    # sender = forms.EmailField(label="Sender's Email Address")
    subject = forms.CharField(required=False, label="Subject")
    message = forms.CharField(widget=forms.Textarea, label="Message Content")
    keyword = forms.CharField(required=False, label="GIF Keyword")
    language = forms.ChoiceField(choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('it', 'Italian'), ('he', 'Hebrew'), ('zh', 'Mandarin')], label="Language")
