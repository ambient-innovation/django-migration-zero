from django.contrib import admin

from migration_zero.models import MigrationZeroConfiguration


@admin.register(MigrationZeroConfiguration)
class MigrationZeroAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "migration_imminent",
        "migration_date",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
