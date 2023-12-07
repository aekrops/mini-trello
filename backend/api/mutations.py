import logging
import graphene

from utils.base_classes import BaseMutation

from api.queries import CardType, ListType
from api.models import Card, List

from api.inputs import (
    CreateCardInput, UpdateCardInput, DeleteCardInput,
    CreateListInput, UpdateListNameInput, UpdateListItemsInput, DeleteListInput, DeleteListItemByCardIdInput
)


logger = logging.getLogger(__name__)


class CreateList(BaseMutation):
    class Arguments:
        input = CreateListInput(required=True)

    list = graphene.Field(lambda: ListType)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            list_instance = List(name=input.name)
            list_instance.save()
            return cls.success(list=list_instance)
        except Exception as e:
            return cls.failure(error_message=str(e))


class UpdateListName(BaseMutation):
    class Arguments:
        input = UpdateListNameInput(required=True)

    list = graphene.Field(lambda: ListType)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            List.update_name(current_name=input.current_name, new_name=input.new_name)
            updated_list = List(name=input.new_name)
            return cls.success(list=updated_list)
        except Exception as e:
            return cls.failure(error_message=str(e))


class UpdateListItems(BaseMutation):
    class Arguments:
        input = UpdateListItemsInput(required=True)

    list = graphene.Field(lambda: ListType)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            List.update_items(list_name=input.list_name, items=input.items)
            updated_list = List(name=input.list_name, items=input.items)
            return cls.success(list=updated_list)
        except Exception as e:
            return cls.failure(error_message=str(e))


class DeleteListItemByCardId(BaseMutation):
    class Arguments:
        input = DeleteListItemByCardIdInput(required=True)

    list = graphene.Field(lambda: ListType)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            List.delete_item_card_by_id(list_name=input.list_name, card_id=input.card_id)
            return cls.success()
        except Exception as e:
            return cls.failure(error_message=str(e))


class DeleteList(BaseMutation):
    class Arguments:
        input = DeleteListInput(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        try:
            List.delete(name=input.name)
            return cls.success()
        except Exception as e:
            return cls.failure(error_message=str(e))


class CreateCard(BaseMutation):
    class Arguments:
        input = CreateCardInput(required=True)

    card = graphene.Field(lambda: CardType)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            card = Card(**input)
            card.save()
            return cls.success(card=card)
        except Exception as e:
            return cls.failure(error_message=str(e))


class UpdateCard(BaseMutation):
    class Arguments:
        input = UpdateCardInput(required=True)

    card = graphene.Field(lambda: CardType)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            card_id = input.pop('card_id')
            Card.update(card_id, **input)
            updated_card = next((card for card in Card.all() if card['card_id'] == card_id), None)
            return cls.success(card=CardType(**updated_card)) if updated_card else None
        except Exception as e:
            logger.error(f"Error editing card: {e}")
            return cls.failure(error_message="Failed to edit card.")


class DeleteCard(BaseMutation):
    class Arguments:
        input = DeleteCardInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            card_id = input.pop('card_id')
            Card.delete(card_id)
            return cls.success()
        except Exception as e:
            logger.error(f"Error deleting card: {e}")
            return cls.failure(error_message="Failed to delete card.")


class Mutation(graphene.ObjectType):
    # for list
    create_list = CreateList.Field()
    update_list_name = UpdateListName.Field()
    update_list_items = UpdateListItems.Field()
    delete_list_item_by_card_id = DeleteListItemByCardId.Field()
    delete_list = DeleteList.Field()
    # for list
    create_card = CreateCard.Field()
    update_card = UpdateCard.Field()
    delete_card = DeleteCard.Field()
