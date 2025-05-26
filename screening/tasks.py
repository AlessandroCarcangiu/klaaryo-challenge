import time
import requests
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from email_validator import validate_email, EmailNotValidError
from .models import Candidate, Check


@shared_task
def test_task():
    print("Celery Test")
    return "OK"


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=10,
    retry_kwargs={'max_retries': 3}
)
def run_screening(self, candidate_id: str):
    print(f"{time.gmtime()} - Start screening for candidate with id: {candidate_id}")

    try:
        status = "checked"
        results = []

        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except ObjectDoesNotExist:
            raise f"ERROR - Run Screening Task - candidate {candidate_id} not found"

        # check email format
        result_format = "Passed"
        try:
            validate_email(candidate.email, check_deliverability=False)
        except EmailNotValidError as e:
            result_format = f"Email format not valid - {e}"
            status = "rejected"
        results.append(
            Check("format", result_format).to_dict()
        )

        # check duplicate email
        result_duplicates = "No duplicates"
        normalized_email, domain = normalize_email(candidate.email)

        qs = Candidate.objects.exclude(id=candidate.id)
        if domain.lower().startswith("gmail"):
            other_candidates = Candidate.objects.exclude(id=candidate.id)
            qs = qs.filter(id__in=[
                c.id for c in other_candidates
                if normalize_email(c.email)[0] == normalized_email
            ]).count()
        else:
            qs = qs.filter(email__iexact=normalized_email).count()

        if qs > 0:
            result_duplicates = f"Found {qs} duplicates"
            status = "rejected"
        results.append(
            Check("duplicates", result_duplicates).to_dict()
        )

        # update candidate
        candidate.status = status
        candidate.screening_log = results
        candidate.save()

        # send message to azure mock service
        send_to_azure(str(candidate.id), candidate.status, candidate.screening_log)

    except Exception as e:
        raise self.retry(exc=e)

    return f"{time.gmtime()} - Screening complete for candidate with id: {candidate_id}"


def normalize_email(email: str) -> (str, str):
    email = email.strip().lower()
    local, _, domain = email.partition('@')
    if domain.lower().startswith("gmail"):
        local = local.replace(".", "").replace("+", "")
    return f"{local}@{domain}", domain


def send_to_azure(candidate_id: str, status: str, screening_result: list):
    try:
        response = requests.post(
            "http://azure-mock.local/api/events",
            json={
                "candidate_id": str(candidate_id),
                "status": status,
                "screening_result": screening_result
            },
            timeout=5
        )
        response.raise_for_status()
        print(f"Azure communication success: {response.status_code}")
    except requests.RequestException as e:
        print(f"Azure communication failed: {e}")
