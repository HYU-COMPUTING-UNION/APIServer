import graphql_social_auth
import graphene
import re

from api.decorators import login_required, method_decorator
from api.exceptions import InvalidInputError

from django.contrib.auth import get_user_model, logout, login, authenticate
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from graphene_django import DjangoObjectType

from .models import Profile, EmailAuth
from .tasks import send_confirmation_mail
from .tokens import make_token

# ObjectTyes


class UserNode(DjangoObjectType):
    is_email_authenticated = graphene.Boolean(
        required=True, source='is_email_authenticated')

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
        try:
            social.user.email_auth
        except EmailAuth.DoesNotExist:
            while True:
                try:
                    EmailAuth.objects.create(
                        user=social.user, token=make_token())
                    break
                except IntegrityError:
                    pass
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


class SendEmailAuth(graphene.relay.ClientIDMutation):
    state = graphene.Boolean(required=True)

    class Input:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    @method_decorator(login_required)
    def mutate_and_get_payload(self, info, **input):
        name = input.get('name')
        email = input.get('email')

        p = re.compile(r'^[a-zA-Z0-9_.+-]+@hanyang\.ac\.kr$')

        if not p.match(email):
            raise InvalidInputError(message=_('invalid email'))

        user = info.context.user

        try:
            profile = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(name=name, email=email)
        user.profile = profile
        user.save()

        if user.profile.name != name:
            raise InvalidInputError(message=_('name does not match'))

        message = render_to_string('email_auth.html', {
            'user': user.profile,
            'token': user.email_auth.token,
        })

        send_confirmation_mail.delay(
            '이메일 확인',
            message,
            from_email='한양소융 <no-reply@hycomputing.org>',
            recipients=[email],
        )

        return SendEmailAuth(state=True)


class AuthenticateEmail(graphene.relay.ClientIDMutation):
    state = graphene.Boolean(required=True)

    class Input:
        token = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **input):
        token = input.get('token')

        try:
            email_auth = EmailAuth.objects.get(token=token)
            email_auth.is_email_authenticated = True
            email_auth.save()
            return AuthenticateEmail(state=True)

        except EmailAuth.DoesNotExist:
            raise InvalidInputError(message=_('invalid token'))


# Query and Mutation


class Query:
    viewer = graphene.Field(UserNode)

    @method_decorator(login_required)
    def resolve_viewer(self, info, **args):
        return info.context.user


class Mutation:
    social_auth = SocialAuth.Field(description=_('Social authentication'), )
    logout = Logout.Field()
    login = Login.Field()
    send_email_auth = SendEmailAuth.Field()
    authenticate_email = AuthenticateEmail.Field()
