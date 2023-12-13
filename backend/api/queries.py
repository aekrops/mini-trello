from datetime import datetime

import graphene

# from graphene_django.types import DjangoObjectType

from api.models import List, Card, Label

from utils.date_utils import convert_iso_to_datetime


class ListType(graphene.ObjectType):
    name = graphene.String()
    items = graphene.List(graphene.String)


class CardType(graphene.ObjectType):
    card_id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    list_name = graphene.String()
    due_date = graphene.String()
    created_at = graphene.DateTime()
    labels = graphene.List(graphene.String)

    def resolve_created_at(self, info):
        return convert_iso_to_datetime(self.get("created_at"))


class LabelType(graphene.ObjectType):
    name = graphene.String()


class Query(graphene.ObjectType):
    all_lists = graphene.List(ListType)
    all_cards = graphene.List(CardType)
    get_list_by_name = graphene.Field(ListType, name=graphene.String(required=True))
    grouped_cards_by_list_name = graphene.Field(graphene.JSONString)
    all_labels = graphene.List(LabelType)

    def resolve_all_lists(self, info):
        return List.all()

    def resolve_all_cards(self, info):
        return Card.all()

    def resolve_get_list_by_name(self, info, name: str):
        list_data = List.get_by_name(name)  # Replace with your method to fetch the list by name
        if list_data:
            return list_data
        else:
            return None

    def resolve_grouped_cards_by_list_name(self, info):
        return Card.all_grouped_by_list_name()

    def resolve_all_labels(self, info):
        return Label.all()
