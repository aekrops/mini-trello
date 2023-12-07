import graphene

from api.mutations import Mutation as CardMutation
from api.queries import Query as CardQuery


schema = graphene.Schema(query=CardQuery, mutation=CardMutation)
