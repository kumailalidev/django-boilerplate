from django.shortcuts import render

from .models import Greeting, Image


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


def images(request):
    if request.method.lower() == "post":
        image = request.FILES.get("image")
        Image.objects.create(image=image)

        return render(request, "greetings/images.html", {"images": Image.objects.all()})

    return render(request, "greetings/images.html", {"images": Image.objects.all()})
