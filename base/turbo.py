from django.http import HttpResponse
from django.template.loader import render_to_string


class TurboStreamMixin:
    """
    Mixin to provide Turbo Stream responses for Django views.
    """

    def turbo_stream_response(
        self, action, target, content="", template=None, context=None
    ):
        """
        Generate a Turbo Stream response.

        Actions: append, prepend, replace, update, remove
        """
        if template and context:
            content = render_to_string(template, context, request=self.request)

        turbo_stream = f"""
        <turbo-stream action="{action}" target="{target}">
            <template>{content}</template>
        </turbo-stream>
        """

        return HttpResponse(turbo_stream, content_type="text/vnd.turbo-stream.html")

    def is_turbo_request(self):
        """Check if the request is from Turbo."""
        return self.request.headers.get("Accept", "").startswith(
            "text/vnd.turbo-stream"
        )


def turbo_stream(action, target, content="", template=None, context=None, request=None):
    """
    Standalone function to generate Turbo Stream responses.
    """
    if template and context and request:
        content = render_to_string(template, context, request=request)

    turbo_stream = f"""
    <turbo-stream action="{action}" target="{target}">
        <template>{content}</template>
    </turbo-stream>
    """

    return HttpResponse(turbo_stream, content_type="text/vnd.turbo-stream.html")
