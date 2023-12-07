export interface Card {
    cardId: string;
    title: string;
    description: string;
    listName: string;
    dueDate: string;
    createAt: string;
    labels: string[];
}

export interface AllCards {
    allCards: Card[]
}