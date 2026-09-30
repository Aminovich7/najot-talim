from django import forms


class PublishMessageForm(forms.Form):
    message = forms.CharField(
        label="Message",
        max_length=500,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Type a message for RabbitMQ",
                "autocomplete": "off",
            }
        ),
    )
