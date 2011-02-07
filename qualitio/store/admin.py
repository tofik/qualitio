from django.contrib import admin
from qualitio.store import models
from qualitio import core


class TestCaseInline(core.PathModelInline):
    model = models.TestCase


class TestCaseDirectoryAdmin(core.DirectoryModelAdmin):
    inlines = [ TestCaseInline ]
admin.site.register(models.TestCaseDirectory, TestCaseDirectoryAdmin)


class TestCaseStepInline(admin.TabularInline):
    model = models.TestCaseStep
    extra = 1


class AttachmentInline(admin.TabularInline):
    model = models.Attachment
    extra = 1


class TestCaseAdmin(core.PathModelAdmin):
    inlines = [ TestCaseStepInline,
                AttachmentInline ]
admin.site.register(models.TestCase, TestCaseAdmin)

