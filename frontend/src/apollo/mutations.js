import { gql } from '@apollo/client';

export const DELETE_CARD_MUTATION = gql`
  mutation DeleteCard($cardId: String!) {
    deleteCard(input: { cardId: $cardId }) {
      ok
    }
  }
`;

export const UPDATE_LIST_ITEMS_MUTATION = gql`
  mutation UpdateListItems($listName: String!, $items: [String!]!) {
    updateListItems(input: { listName: $listName, items: $items }) {
      ok
      errorMessage
    }
  }
`;

export const DELETE_LIST_ITEM_BY_CARD_ID_MUTATION = gql`
  mutation DeleteListItemByCardId($listName: String!, $cardId: String!) {
    deleteListItemByCardId(input: { listName: $listName, cardId: $cardId }) {
      ok
      errorMessage
    }
  }
`;

export const CREATE_CARD_MUTATION = gql`
  mutation CreateCard($title: String!, $description: String!, $listName: String!) {
    createCard(
      input: {
        title: $title
        description: $description
        listName: $listName
       }
     ) {
        card {
            cardId
            title
            description
            listName
        }
        ok
        errorMessage
    }
}
`

export const UPDATE_CARD_MUTATION = gql`
  mutation UpdateCard($cardId: String!, $title: String!, $description: String!, $dueDate: String!) {
    updateCard(
        input: {
            cardId: $cardId
            title: $title
            description: $description
            dueDate: $dueDate
        }
    ) {
        ok
        errorMessage
    }
} 
`;

export const CREATE_LIST_MUTATION = gql`
  mutation CreateList($name: String!) {
      createList(
        input: {
          name: $name
        }
      ) {
        list {
            name
            items
        }
        ok
        errorMessage
      }
  }
`;

export const DELETE_LIST_MUTATION = gql`
  mutation DeleteCard($name: String!) {
    deleteList(input: { name: $name }) {
      ok
    }
  }
`;