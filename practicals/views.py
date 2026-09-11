from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Subject, Practical


def home(request):
    subjects = Subject.objects.all()

    return render(
        request,
        "home/index.html",
        {
            "subjects": subjects
        }
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
            "practicals": practicals
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
            "practical": practical
        }
    )


@login_required
def dashboard(request):

    subjects = Subject.objects.all()
    practicals = Practical.objects.all()

    total_subjects = subjects.count()
    total_practicals = practicals.count()

    total_qr_codes = subjects.exclude(
        qr_code=""
    ).count()

    recent_subjects = subjects.order_by(
        "-created_at"
    )[:5]

    recent_practicals = practicals.select_related(
        "subject"
    ).order_by(
        "-created_at"
    )[:5]

    context = {
        "total_subjects": total_subjects,
        "total_practicals": total_practicals,
        "total_qr_codes": total_qr_codes,
        "recent_subjects": recent_subjects,
        "recent_practicals": recent_practicals,
    }

    return render(
        request,
        "dashboard.html",
        context
    )


def qr_print(request, subject_id):
    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    return render(
        request,
        "practicals/qr_print.html",
        {
            "subject": subject,
        }
    )