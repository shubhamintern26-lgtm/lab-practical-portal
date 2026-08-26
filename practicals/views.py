from django.shortcuts import render, get_object_or_404
from .models import Subject, Practical


def home(request):
    subjects = Subject.objects.all()

    return render(
        request,
        "home/index.html",
        {"subjects": subjects}
    )


def subject_detail(request, subject_id):
    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    practicals = subject.practicals.all()

    return render(
        request,
        "practicals/subject_detail.html",
        {
            "subject": subject,
            "practicals": practicals,
        }
    )


def practical_detail(request, practical_id):
    practical = get_object_or_404(
        Practical,
        id=practical_id
    )

    return render(
        request,
        "practicals/practical_detail.html",
        {
            "practical": practical,
        }
    )