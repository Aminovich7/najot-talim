from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect, render

from messaging.forms import PublishMessageForm
from messaging.rabbitmq import consume_one_message, publish_message


def home(request):
    return render(
        request,
        "messaging/home.html",
        {
            "form": PublishMessageForm(),
            "queue_name": settings.RABBITMQ_QUEUE_NAME,
            "rabbitmq_host": settings.RABBITMQ_HOST,
            "rabbitmq_port": settings.RABBITMQ_PORT,
        },
    )


def publish_message_view(request):
    if request.method != "POST":
        return redirect("home")

    form = PublishMessageForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Enter a message before publishing.")
        return redirect("home")

    message = form.cleaned_data["message"]
    try:
        publish_message(message)
    except Exception as exc:  # pragma: no cover - surfaced in the UI
        messages.error(request, f"Publish failed: {exc}")
    else:
        messages.success(request, f"Published message: {message}")
    return redirect("home")


def consume_message_view(request):
    if request.method != "POST":
        return redirect("home")

    try:
        consumed = consume_one_message()
    except Exception as exc:  # pragma: no cover - surfaced in the UI
        messages.error(request, f"Consume failed: {exc}")
    else:
        if consumed is None:
            messages.warning(request, "Queue is empty.")
        else:
            messages.success(request, f"Consumed message: {consumed.body}")
    return redirect("home")
