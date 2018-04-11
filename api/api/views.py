from graphql_jwt.exceptions import GraphQLJWTError
from graphene_django.views import GraphQLView
from .exceptions import APIError


class CustomGraphQLView(GraphQLView):

    @staticmethod
    def format_error(error):
        if hasattr(error, 'original_error') and error.original_error:
            formatted = {"message": str(error.original_error)}
            if isinstance(error.original_error, APIError):
                formatted['code'] = error.original_error.code
            elif isinstance(error.original_error, GraphQLJWTError):
                formatted['code'] = 401
            return formatted

        return GraphQLView.format_error(error)
