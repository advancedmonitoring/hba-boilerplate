import logging

from django.utils.translation import get_language_from_request

from {PROJECT_NAME}.users.models import Language

logger = logging.getLogger(__name__)


class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if not user.is_anonymous:
            request_lang = get_language_from_request(request=request).lower()
            if request_lang in Language.values:
                if request_lang != user.language:
                    user.language = request_lang
                    user.save()
            else:
                logger.warning("Invalid language code")
        response = self.get_response(request)

        return response
