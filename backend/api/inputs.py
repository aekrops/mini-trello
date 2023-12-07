import graphene


class CreateCardInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String()
    list_name = graphene.String()
    due_date = graphene.String()


class UpdateCardInput(graphene.InputObjectType):
    card_id = graphene.String(required=True)
    title = graphene.String()
    description = graphene.String()
    list_name = graphene.String()
    due_date = graphene.String()
    labels = graphene.List(graphene.String)


class DeleteCardInput(graphene.InputObjectType):
    card_id = graphene.String(required=True)


class CreateListInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class UpdateListNameInput(graphene.InputObjectType):
    current_name = graphene.String(required=True)
    new_name = graphene.String(required=True)


class UpdateListItemsInput(graphene.InputObjectType):
    list_name = graphene.String(required=True)
    items = graphene.List(graphene.String, required=True)


class DeleteListItemByCardIdInput(graphene.InputObjectType):
    list_name = graphene.String(required=True)
    card_id = graphene.String(required=True)


class DeleteListInput(graphene.InputObjectType):
    name = graphene.String(required=True)
