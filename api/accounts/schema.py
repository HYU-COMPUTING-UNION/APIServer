import graphql_social_auth
import graphene

from api.decorators import login_required, method_decorator

from django.contrib.auth import get_user_model, logout, login, authenticate
from django.utils.translation import gettext_lazy as _

from graphene_django import DjangoObjectType

from .models import Profile, AffiliationAuth


# ObjectTyes

class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node, )
        exclude_fields = ['password']


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        interfaces = (graphene.relay.Node, )


# Mutation fields

class SocialAuth(graphql_social_auth.relay.mutations.SocialAuthMutation):
    viewer = graphene.Field(UserNode)

    @classmethod
    def resolve(cls, root, info, social, **kwargs):
        return cls(viewer=social.user)


class Login(graphene.relay.ClientIDMutation):
    viewer = graphene.Field(UserNode)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **input):
        username = input.get('username')
        password = input.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(info.context, user)
            return Login(viewer=user)

        return Login()


class Logout(graphene.relay.ClientIDMutation):
    state = graphene.Boolean(required=True)

    @method_decorator(login_required)
    def mutate_and_get_payload(self, info, **input):
        logout(info.context)
        return Logout(state=True)


class Authenticate(graphene.relay.ClientIDMutation):
    state = graphene.Boolean(required=True)

    class Input:
        name = graphene.String(required=True)
        student_id = graphene.String(required=True)

    @method_decorator(login_required)
    def mutate_and_get_payload(self, info, **input):
        name = input.get('name')
        student_id = input.get('student_id')
        state = AffiliationAuth.objects.filter(
                    name=name,
                    student_id=student_id,
                ).exists()
        user = info.context.user

        if state:
            try:
                profile = Profile.objects.get(name=name, student_id=student_id)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(
                    name=name, student_id=student_id,
                    is_affiliation_authenticated=True,
                )
            user.profile = profile
            user.save()

        return Authenticate(state=state)


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
    login = Login.Field()
    authenticate = Authenticate.Field()
