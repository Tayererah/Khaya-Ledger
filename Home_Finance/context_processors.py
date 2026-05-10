from bills.models import Bill
from datetime import date


def notifications(request):
    if request.user.is_authenticated:
        try:
            today = date.today()
            household = request.user.member.household
            upcoming = Bill.objects.filter(
                household=household,
                is_active=True,
                due_day__gte=today.day,
                due_day__lte=today.day + 7
            ).order_by('due_day')
            return {'upcoming_bills_notif': upcoming}
        except Exception:
            return {'upcoming_bills_notif': []}
    return {'upcoming_bills_notif': []}