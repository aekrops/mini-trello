import React from 'react';
import Card from './Card';
import {
    Card as CardProps
} from '../types/card'
import { Droppable } from 'react-beautiful-dnd';

interface ListProps {
    listName: string;
    cards: CardProps[];
    onDeleteList: (listName: string) => void;
    onDeleteCard: (cardId: string) => void;
}

function List({ listName, cards, onDeleteList, onDeleteCard } : ListProps) {
    const handleDelete = () => {
        onDeleteList(listName)
    }
    
    return (
        <Droppable droppableId={listName}>
            {(provided) => (
                <div ref={provided.innerRef} {...provided.droppableProps} className="bg-gray-100 p-3 rounded w-64">
                    <div className="flex justify-between">
                        <h2 className="font-bold mb-2">{listName}</h2>
                        <button onClick={handleDelete} className="text-red-500 hover:text-red-700 mr-1.5 w-5 h-5">
                            ✕
                        </button>
                    </div>
                    {cards.map((card, index) => (
                        <Card key={card.cardId} card={card} index={index} onDeleteCard={onDeleteCard}/>
                        ))}
                    {provided.placeholder}
                </div>
                )}
        </Droppable>
        );
}

export default List;
