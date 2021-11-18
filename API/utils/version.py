from rest_framework.versioning import BaseVersioning


class GetParamVersion(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get('version')
        return version
