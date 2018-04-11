import graphene


class Query(
    graphene.ObjectType,
):
    node = graphene.relay.Node.Field()


class Mutation(
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, )
