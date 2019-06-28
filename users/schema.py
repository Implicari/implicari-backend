import graphene
import graphql_jwt


class Mutation(graphene.ObjectType):
    refresh_token = graphql_jwt.Refresh.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
