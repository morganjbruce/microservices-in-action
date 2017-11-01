import json
from nameko.web.handlers import http
from werkzeug.wrappers import Response


class HttpDemoService:
    name = "http_demo_service"

    @http('GET', '/books/<string:uuid>')
    def demo_get(self, request, uuid):
        data = {'id': uuid, 'title': 'The unbearable lightness of being',
                'author': 'Milan Kundera'}
        return Response(json.dumps({'book': data}),
                        mimetype='application/json')

    @http('POST', '/books')
    def demo_post(self, request):
        return Response(json.dumps({'book': request.data.decode()}),
                        mimetype='application/json')
