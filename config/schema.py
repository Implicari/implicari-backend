import graphene

from graphene_django.debug import DjangoDebug

from users.schema import Mutation as UserMutation


class Mutation(UserMutation, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(mutation=Mutation)
