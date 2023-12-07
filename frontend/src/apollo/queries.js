import { gql } from '@apollo/client';

export const ALL_LISTS_QUERY = gql`
  query AllLists {
    allLists {
      name
      items
    }
  }
`;

export const ALL_CARDS_QUERY = gql`
  query AllCards {
    allCards {
      cardId
      title
      description
      listName
      dueDate
      labels
    }
  }
`;

export const ALL_CARDS_BY_LIST_NAME_QUERY = gql`
  query GroupedCardsByListName {
    groupedCardsByListName
  }
`;

export const GET_LIST_BY_NAME_QUERY = gql`
  query GetListByName($name: String!) {
    getListByName(name: $name) {
      items
      name
    }
  }
`;