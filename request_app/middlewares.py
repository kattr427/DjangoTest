from django.http import HttpRequest


def set_useraget_middleware(get_response):

    print('запуск')

    def middleware(request: HttpRequest):

        print('до запроса')

        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)

        print('после запроса')

        return response

    return middleware


class CountRequestsMiddleware:
    def __int__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.response_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('Количество запросов=', self.requests_count)
        response = self.get_response(request)
        self.response_count += 1
        print('Количество ответов=', self.response_count)
        return response