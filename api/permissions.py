from rest_framework import permissions


class IsSuperUserOrTelegramBot(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.username == 'telegram_bot_username'
