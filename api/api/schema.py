import graphene

import accounts.schema
import petitions.schema


class Query(
    graphene.ObjectType,
    accounts.schema.Query,
    petitions.schema.Query,
):
    node = graphene.relay.Node.Field()


class Mutation(
    graphene.ObjectType,
    accounts.schema.Mutation,
    petitions.schema.Mutation,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
