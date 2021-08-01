import json

from django.http import HttpResponse


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """

    def render_to_json(self, context, **kwargs):
        return HttpResponse(
            self.convert_to_json(context), content_type='application/json', **kwargs
        )

    def convert_to_json(self, context):
        return json.dumps(context)
