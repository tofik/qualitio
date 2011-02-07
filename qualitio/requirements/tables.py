import django_tables as tables
from django.utils.safestring import mark_safe
from qualitio.requirements.models import Requirement


class RequirementsFilterTable(tables.ModelTable):
    directory_path = tables.Column(verbose_name="Path")
    checked = tables.Column(verbose_name=" ")

    class Meta:
        model = Requirement

    def render_checked(self, a):
        return mark_safe("<input type='checkbox' />")

    def render_directory_path(self, a):
        return a.get_path()
