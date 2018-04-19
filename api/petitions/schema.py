import graphene

from api.decorators import login_required, method_decorator
from accounts.decorators import auth_required

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


from .models import Petition, Answer, Category


# ObjectTypes

class PetitionNode(DjangoObjectType):
    class Meta:
        model = Petition
        interfaces = (graphene.relay.Node, )
        filter_fields = []


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

    @method_decorator(login_required)
    @method_decorator(auth_required)
    def mutate_and_get_payload(self, info, **input):
        title = input.get('title')
        content = input.get('content')
        issuer = info.context.user.profile

        petition = Petition(title=title, content=content, issuer=issuer)
        petition.save()
        return CreatePetition(petition=petition)


# Query and Mutation

class Query:
    petitions = DjangoFilterConnectionField(PetitionNode)
    answers = DjangoFilterConnectionField(AnswerNode)
    categories = DjangoFilterConnectionField(CategoryNode)


class Mutation:
    create_petition = CreatePetition.Field()
