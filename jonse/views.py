from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from jonse.filters import ListingFilter
from jonse.forms import ListingCreateForm
from jonse.models import Listing
from jonse.tables import ListingTable


# Create your views here.
class HomeView(SingleTableMixin, FilterView):
    table_class = ListingTable
    queryset = Listing.objects.for_home()
    paginate_by = 15
    filterset_class = ListingFilter

    def get_template_names(self):

        if self.request.htmx:
            template_name = "home_partial.html"
        else:
            template_name = "home.html"

        return template_name


class MyListingView(LoginRequiredMixin, HomeView):
    redirect_field_name = "next"

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_listings"] = True
        return context


class ListingCreateView(LoginRequiredMixin, CreateView):
    redirect_field_name = "next"
    template_name = "listing/create.html"
    form_class = ListingCreateForm
    success_url = reverse_lazy("my_listings")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
