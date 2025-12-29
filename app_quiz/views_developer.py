# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Quiz, QuizCategory

@csrf_exempt
def import_quizzes(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    created_quizzes = 0
    skipped_categories = []

    for category_data in data:
        category_name = category_data.get("category")
        if not category_name:
            continue  # skip if no category

        try:
            # Only get existing category
            category_obj = QuizCategory.objects.get(slug=category_name.lower())
        except QuizCategory.DoesNotExist:
            skipped_categories.append(category_name)
            continue  # skip this category

        quizzes = category_data.get("quizzes", [])
        for quiz in quizzes:
            question = quiz.get("question")
            optA = quiz.get("optA")
            optB = quiz.get("optB")
            optC = quiz.get("optC")
            optD = quiz.get("optD")
            correct_ans = quiz.get("correct_ans")

            if not all([question, optA, optB, optC, optD, correct_ans]):
                continue  # skip incomplete quizzes

            Quiz.objects.create(
                category=category_obj,
                question=question,
                optA=optA,
                optB=optB,
                optC=optC,
                optD=optD,
                correct_ans=correct_ans.upper()
            )
            created_quizzes += 1

    return JsonResponse({
        "status": "success",
        "created_quizzes": created_quizzes,
        "skipped_categories": skipped_categories
    })
