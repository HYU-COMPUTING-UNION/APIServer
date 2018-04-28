import graphene

from api.decorators import login_required, method_decorator
from api.exceptions import InvalidInputError

from api.types import CountingObjectType

from accounts.decorators import auth_required

from django.utils.translation import gettext_lazy as _

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphql_relay import from_global_id

from .models import Petition, Answer, Category

# ObjectTypes


class PetitionNode(CountingObjectType):
    assentient_count = graphene.Int(required=True, source='assentient_count')
    is_expired = graphene.Boolean(required=True, source='is_expired')
    is_answered = graphene.Boolean(required=True, source='is_answered')

    class Meta:
        model = Petition
        interfaces = (graphene.relay.Node, )
        filter_fields = []
        exclude_fields = ['issuer', 'assentients']

    def resolve_issued_at(self, *args, **kwargs):
        return self.issued_at.date()


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        interfaces = (graphene.relay.Node, )
        filter_fields = []


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (graphene.relay.Node, )
        filter_fields = []


# Mutation fields


class CreatePetition(graphene.relay.ClientIDMutation):
    petition = graphene.Field(PetitionNode)

    class Input:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        category_id = graphene.ID()

    @method_decorator(login_required)
    @method_decorator(auth_required)
    def mutate_and_get_payload(self, info, **input):
        title = input.get('title')
        content = input.get('content')
        category_id = input.get('category_id')
        issuer = info.context.user.profile

        if category_id is not None:
            type_name, _id = from_global_id(category_id)

            if type_name != 'CategoryNode':
                raise InvalidInputError(message=_('categoryId is not valid'))

            try:
                category = Category.objects.get(pk=_id)
            except Category.DoesNotExist:
                raise InvalidInputError(message=_('categoryId is not valid'))
        else:
            category = None

        petition = Petition(title=title, content=content, issuer=issuer)
        petition.save()

        if category is not None:
            petition.categories.add(category)

        return CreatePetition(petition=petition)


class AgreePetition(graphene.relay.ClientIDMutation):
    state = graphene.Boolean(required=True)

    class Input:
        petition_id = graphene.ID(required=True)

    @method_decorator(login_required)
    @method_decorator(auth_required)
    def mutate_and_get_payload(self, info, **input):
        petition_id = input.get('petition_id')
        user = info.context.user.profile

        type_name, _id = from_global_id(petition_id)

        if type_name != 'PetitionNode':
            raise InvalidInputError(message=_('petitionId is not valid'))

        try:
            petition = Petition.objects.get(pk=_id)
        except Petition.DoesNotExist:
            raise InvalidInputError(message=_('petitionId is not valid'))

        petition.assentients.add(user)

        return AgreePetition(state=True)


# Query and Mutation


class Query:
    petitions = DjangoFilterConnectionField(
        PetitionNode,
        is_answered=graphene.Boolean(),
    )
    answers = DjangoFilterConnectionField(AnswerNode)
    categories = DjangoFilterConnectionField(CategoryNode)

    def resolve_petitions(self, info, **input):
        is_answered = input.get('is_answered')
        if is_answered is None:
            return Petition.objects.all()
        else:
            return [
                p for p in Petition.objects.all()
                if p.is_answered == is_answered
            ]


class Mutation:
    create_petition = CreatePetition.Field()
    agree_petition = AgreePetition.Field()
