import graphene

from graphene_django.debug import DjangoDebug

from classrooms.schema import Query as ClassroomQuery
from classrooms.schema import Mutation as ClassroomMutation
from users.schema import Mutation as UserMutation


class Query(ClassroomQuery, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(ClassroomMutation, UserMutation, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query, mutation=Mutation)
