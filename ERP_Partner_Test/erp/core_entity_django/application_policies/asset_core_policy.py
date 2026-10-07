from rest_framework.exceptions import PermissionDenied


PERMISSIONS = {
    "create": "core_entity_django.create_far_assets",
    "view": "core_entity_django.view_far_assets",
    "edit": "core_entity_django.update_far_assets",
    "delete": "core_entity_django.delete_far_assets",
    "validate": "core_entity_django.validate_far_assets",
    "bulk_validate": "core_entity_django.bulk_validate_far_assets",
    "print": "core_entity_django.print_far_assets",
    "import": "core_entity_django.import_far_assets",
    "wip_transfer": "core_entity_django.wip_transfer_far_assets",
    "capitalize": "core_entity_django.capitalize_far_assets",
    "bulk_capitalize": "core_entity_django.bulk_capitalize_far_assets",
    "bulk_delete": "core_entity_django.bulk_delete_far_assets",
    "export": "core_entity_django.export_far_assets",
    "approve": "core_entity_django.approve_far_assets",
}


def has_permission(user, action):
    if not user or not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return user.has_perm(PERMISSIONS[action])


# def require_permission(user, action):
#     if not has_permission(user, action):
#         raise PermissionDenied(
#             f"Permission denied: {PERMISSIONS[action]}"
#         )

def require_permission(user, action):
    return True