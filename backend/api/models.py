import uuid
import logging
from collections import defaultdict
from datetime import datetime
from typing import Optional, Dict, Any
from typing import List as Lt
from operator import itemgetter

from boto3.dynamodb.conditions import Key
from utils.dynamodb import get_dynamodb_table, get_items_by_table

logger = logging.getLogger(__name__)


class List:
    def __init__(self, name: str, items: Lt[Any] = None):
        self.name = name
        self.items = items or []

    def save(self) -> None:
        """Saves the list to the DynamoDB"""
        try:
            table = get_dynamodb_table('Lists')
            item = {"name": self.name, "items": self.items}
            table.put_item(Item=item)
        except Exception as e:
            logger.error(f"Error saving list {e}")

    @classmethod
    def get_by_name(cls, list_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a list by its name from the DynamoDB table."""
        try:
            table = get_dynamodb_table('Lists')
            response = table.get_item(Key={'name': list_name})
            item = response.get('Item')

            if item:
                # Convert the DynamoDB item format to the List class format, if necessary
                return {'name': item['name'], 'items': item.get('items', [])}
            else:
                return None
        except Exception as e:
            logger.error(f"Error retrieving list '{list_name}': {e}")
            raise

    @classmethod
    def update_name(cls, current_name: str, new_name: str) -> None:
        """Update the name of an existing list in the DynamoDB table."""
        try:
            table = get_dynamodb_table('Lists')
            item = table.get_item(Key={'name': current_name}).get('Item')
            new_item = List(name=new_name, items=item.get('items', None))
            new_item.save()
            cls.delete(current_name)

        except Exception as e:
            logger.error(f"Error updating list '{current_name}': {e}")
            raise

    @classmethod
    def update_items(cls, list_name: str, items: Lt[str]) -> None:
        """Update the items of an existing list in the DynamoDB table."""
        try:
            table = get_dynamodb_table('Lists')
            formatted_items = [str(item) for item in items]

            response = table.update_item(
                Key={'name': list_name},
                UpdateExpression="set #it = :items",
                ExpressionAttributeNames={'#it': 'items'},
                ExpressionAttributeValues={':items': formatted_items},
                ReturnValues="UPDATED_NEW"
            )
            logger.info(f"Update response: {response}")
        except Exception as e:
            logger.error(f"Error updating items for list '{list_name}': {e}")
            raise

    @classmethod
    def delete_item_card_by_id(cls, list_name: str, card_id: str) -> None:
        try:
            table = get_dynamodb_table('Lists')
            response = table.get_item(Key={'name': list_name})
            instance = response.get('Item')
            items = instance.get("items", None)

            item_index = next((i for i, item in enumerate(items) if item == card_id), None)

            if item_index is not None:
                items.pop(item_index)

                response = table.update_item(
                    Key={'name': list_name},
                    UpdateExpression="set #it = :items",
                    ExpressionAttributeNames={'#it': 'items'},
                    ExpressionAttributeValues={':items': items},
                    ReturnValues="UPDATED_NEW"
                )
                logger.info(f"Update response: {response}")
            else:
                logger.info(f"Card ID {card_id} not found in list {list_name}.")
        except Exception as e:
            logger.error(f"Error with deleting item by id {e}")
            raise


    @classmethod
    def delete(cls, name: str) -> None:
        """Delete a list from the DynamoDB table."""
        try:
            table = get_dynamodb_table('Lists')
            table.delete_item(Key={'name': name})
            logger.info(f"List '{name}' deleted successfully.")
        except Exception as e:
            logger.error(f"Error deleting list '{name}': {e}")
            raise

    @staticmethod
    def all() -> Lt[Dict[str, Any]]:
        """Retrieve all lists from the DynamoDB table or create default if empty."""
        try:
            items = get_items_by_table('Lists')

            if not items:
                default_list = List(name="To Do")
                default_list.save()
                items = [{'name': default_list.name}]
            return items
        except Exception as e:
            logger.error(f"Error retrieving all lists: {e}")
            raise


class Card:
    def __init__(
        self,
        title: str,
        card_id: str = None,
        description: Optional[str] = None,
        list_name: Optional[str] = "To Do",
        due_date=None
    ):
        self.card_id = card_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.list_name = list_name
        self.due_date = due_date
        self.created_at = datetime.now()
        self.labels = []

    def save(self) -> None:
        """Save the card to the DynamoDB table."""
        try:
            table = get_dynamodb_table('Cards')
            item = {
                'card_id': self.card_id,
                'title': self.title,
                'description': self.description,
                'list_name': self.list_name,
                'due_date': str(self.due_date) if self.due_date else None,
                'created_at': self.created_at.isoformat(),
                'labels': self.labels,
            }
            table.put_item(Item=item)
        except Exception as e:
            logger.error(f"Error saving card: {e}")
            raise

    @classmethod
    def update(cls, card_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Edit an existing card in the DynamoDB table."""
        try:
            table = get_dynamodb_table('Cards')
            update_expression = "set " + ", ".join(f"{k}=:{k}" for k in kwargs)
            expression_attribute_values = {f":{k}": v for k, v in kwargs.items()}
            response = table.update_item(
                Key={'card_id': card_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW"
            )
            return response
        except Exception as e:
            logger.error(f"Error editing card {card_id}: {e}")
            raise

    @classmethod
    def delete(cls, card_id: str) -> None:
        """Delete a card from the DynamoDB table."""
        try:
            table = get_dynamodb_table('Cards')
            table.delete_item(Key={'card_id': card_id})
        except Exception as e:
            logger.error(f"Error deleting card {card_id}: {e}")
            raise

    @staticmethod
    def all() -> Lt[Dict[str, Any]]:
        """Retrieve all cards from the DynamoDB table."""
        try:
            return get_items_by_table('Cards')
        except Exception as e:
            logger.error(f"Error retrieving all cards: {e}")

    @staticmethod
    def all_by_list_name(list_name: str) -> Lt[Dict[str, Any]]:
        """Retrieve all cards with a specific list_name from the DynamoDB table."""
        try:
            table = get_dynamodb_table('Cards')
            response = table.query(
                IndexName='list_name-index',
                KeyConditionExpression=Key('list_name').eq(list_name)
            )
            return response.get('Items', [])
        except Exception as e:
            logger.error(f"Error retrieving cards for list_name {list_name}. Here is error {e}")
            raise

    @staticmethod
    def all_sorted_by_list_name() -> Lt[Dict[str, Any]]:
        """Retrieve all cards and sort them by list_name."""
        try:
            items = get_items_by_table('Cards')
            sorted_items = sorted(items, key=itemgetter("list_name"))
            return sorted_items
        except Exception as e:
            logger.error(f"Error retrieving and sorting cards {e}")
            raise

    @staticmethod
    def all_grouped_by_list_name() -> dict:
        """Retrieve all cards and group them by list_name."""
        try:
            items = get_items_by_table('Cards')

            grouped_by_list_name = defaultdict(list)
            for item in items:
                list_name = item.get('list_name', 'To Do')
                grouped_by_list_name[list_name].append({item["card_id"]: item})

            return dict(grouped_by_list_name)
        except Exception as e:
            print(f"Error retrieving and grouping cards: {e}")
            raise


class Label:
    def __init__(self, name):
        self.name = name

    def save(self) -> None:
        """Save the label to the DynamoDB table."""
        table = get_dynamodb_table('Labels')
        item = {'name': self.name}
        table.put_item(Item=item)

    @staticmethod
    def all() -> Lt[Dict[str, Any]]:
        """Retrieve all labels from the DynamoDB table."""
        try:
            return get_items_by_table('Labels')
        except Exception as e:
            logger.error(f"Error retrieving all labels: {e}")
