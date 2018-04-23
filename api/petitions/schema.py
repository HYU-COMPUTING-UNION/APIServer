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


# Query and Mutation

class Query:
    petitions = DjangoFilterConnectionField(PetitionNode)
    answers = DjangoFilterConnectionField(AnswerNode)
    categories = DjangoFilterConnectionField(CategoryNode)


class Mutation:
    create_petition = CreatePetition.Field()
