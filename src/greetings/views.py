from django.shortcuts import render

from greetings.models import Greeting


def home(request):
    message = "No Message..."

    # get latest greeting obj. from db
    greeting_obj = Greeting.objects.last()

    if greeting_obj:
        message = greeting_obj.message

    context = {
        "message": message,
    }

    return render(
        request=request, template_name="greetings/index.html", context=context
    )
