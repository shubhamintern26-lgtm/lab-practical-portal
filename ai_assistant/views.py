from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from practicals.models import Practical
from .services import ask_ai


@require_POST
def ask_ai_view(request):

    practical_id = request.POST.get("practical_id")
    question = request.POST.get("question", "").strip()

    if not practical_id:
        return JsonResponse(
            {
                "error": "Practical ID is required."
            },
            status=400
        )

    if not question:
        return JsonResponse(
            {
                "error": "Please enter a question."
            },
            status=400
        )

    practical = get_object_or_404(
        Practical,
        id=practical_id
    )

    try:
        answer = ask_ai(
            practical,
            question
        )

        return JsonResponse(
            {
                "answer": answer
            }
        )

    except Exception as e:
        print("AI ERROR:", e)

        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )