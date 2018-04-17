import graphql_social_auth
import graphene

from api.decorators import login_required, method_decorator

from django.contrib.auth import get_user_model, logout
from django.utils.translation import gettext_lazy as _

from graphene_django import DjangoObjectType


# ObjectTyes

class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node, )
        exclude_fields = ['password']


# Mutation fields

class SocialAuth(graphql_social_auth.relay.mutations.SocialAuthMutation):
    viewer = graphene.Field(UserNode)

    @classmethod
    def resolve(cls, root, info, social, **kwargs):
        return cls(viewer=social.user)


class Logout(graphene.relay.ClientIDMutation):
    state = graphene.Boolean(required=True)

    @method_decorator(login_required)
    def mutate_and_get_payload(self, info, **input):
        logout(info.context)
        return Logout(state=True)


# Query and Mutation

class Query:
    viewer = graphene.Field(UserNode)

    @method_decorator(login_required)
    def resolve_viewer(self, info, **args):
        return info.context.user


class Mutation:
    social_auth = SocialAuth.Field(
        description=_('Social authentication'),
    )
    logout = Logout.Field()
