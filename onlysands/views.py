from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.views.generic import DetailView, UpdateView

from onlysands.settings import LIVE

from .forms import RegisterForm, ReviewForm
from .models import Beach, UserProfile, Review


def home(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            user.userprofile.last_confirmation_email_sent_at = now()
            token = get_random_string(32)
            user.userprofile.confirmation_token = token
            user.userprofile.save()

            confirmation_link = request.build_absolute_uri(f"/confirm/{token}/")
            if LIVE:
                send_mail(
                    subject="Confirm Your Onlysands Account Email",
                    message=f"Click here to confirm your email: {confirmation_link}".replace(
                        "http:", "https:"
                    ),
                    from_email="info@andrewkmorrison.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            messages.success(
                request, "Please confirm your email before leaving a review!"
            )
            return redirect("home")
    else:
        form = RegisterForm()

    return render(
        request, "register.html", {"form": form, "timestamp": now().timestamp()}
    )


def confirm_email(request, token):
    try:
        profile = UserProfile.objects.get(confirmation_token=token)
        profile.email_confirmed = True
        profile.confirmation_token = ""
        profile.user.save()
        profile.save()
        messages.success(
            request, "Your email has been confirmed. You can now leave reviews!"
        )
    except UserProfile.DoesNotExist:
        messages.error(request, "Invalid confirmation token.")

    return redirect("home")


def beach_list(request):
    beaches = Beach.objects.values("id", "name", "latitude", "longitude", "rating")
    return JsonResponse(list(beaches), safe=False)



class BeachDetailView(DetailView):
    model = Beach
    template_name = "beach_detail.html"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        beach = self.object
        user = self.request.user

        if user.is_authenticated:
            context['user_review'] = Review.objects.filter(user=user, beach=beach).first()
            if not context['user_review']:
                context['review_form'] = ReviewForm()
            context['other_reviews'] = Review.objects.filter(beach=beach).exclude(user=user)
        else:
            context['user_review'] = None
            context['other_reviews'] = Review.objects.filter(beach=beach)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        beach = self.object

        if not request.user.is_authenticated:
            return redirect("login")

        if Review.objects.filter(user=request.user, beach=beach).exists():
            return redirect("beach-detail", pk=beach.pk)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.beach = beach
            review.save()
            return redirect("beach-detail", pk=beach.pk)

        context = self.get_context_data()
        context['review_form'] = form
        return self.render_to_response(context)

class EditReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "edit_review.html"

    def get_success_url(self):
        return self.object.beach.get_absolute_url()

    def test_func(self):
        return self.get_object().user == self.request.user
        
@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    beach = review.beach
    review.delete()
    return redirect('beach-detail', pk=beach.pk)