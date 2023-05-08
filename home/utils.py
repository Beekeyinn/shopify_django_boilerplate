from django.urls import reverse


def build_home_redirect_uri(request):
    host_domain = request.get_host()
    home = reverse("root_path")
    return f"https://{host_domain}{home}"
