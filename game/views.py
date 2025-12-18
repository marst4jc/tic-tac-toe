from django.shortcuts import render


def home(request):
    """Render the Tic-Tac-Toe interface."""

    return render(request, "game/index.html")
