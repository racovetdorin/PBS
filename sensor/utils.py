from rest_framework.renderers import BrowsableAPIRenderer

SENSOR_DATA_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "object",
            "properties": {
                "attributes": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string"}
                    }
                },
                "data": {"type": "string"},
                "messageId": {"type": "string"},
                "message_id": {"type": "string"},
                "publishTime": {"type": "string"},
                "publish_time": {"type": "string"},
            },
        },
        "subscription": {"type": "string"},
    },
}


class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    """Renders the browsable api, but excludes the forms."""

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)
        ctx['display_edit_forms'] = False
        return ctx

    def show_form_for_method(self, view, method, request, obj):
        """We never want to do this! So just return False."""
        return False

    def get_rendered_html_form(self, data, view, method, request):
        """Why render _any_ forms at all. This method should return
        rendered HTML, so let's simply return an empty string.
        """
        return ""
