import React, { useState } from 'react';
import { Draggable } from 'react-beautiful-dnd';
import { useMutation } from '@apollo/client';
import { UPDATE_CARD_MUTATION } from '../apollo/mutations';
import { ReactComponent as EditIcon} from '../icons/edit.svg';


interface CardProps {
    card: {
        cardId: string;
        title: string;
        description: string;
        listName: string;
        dueDate: string;
        labels: string[];
    };
    index: number;
    onDeleteCard: (cardId: string) => void;
}
function Card({ card, index, onDeleteCard }: CardProps) {
  const [updateCard] = useMutation(UPDATE_CARD_MUTATION, {
    onCompleted: (data) => {
      if (data.updateCard.ok) {
        console.log("Card updated successfully");
      } else {
        console.error("Update failed:", data.updateCard.errorMessage);
      }
    },
    onError: (error) => {
        console.error("Error updating card:", error);
        console.error("Sent variables:", {
          cardId: card.cardId,
          title: title,
          description: description,
          dueDate: dueDate,
        });
      },
  });
  
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(card.title ? card.title : "");
  const [description, setDescription] = useState(card.description ? card.description : "");
  const [dueDate, setDueDate] = useState(card.dueDate ? card.dueDate : "");

  const handleDelete = () => {
    onDeleteCard(card.cardId);
  };
  
  const handleEdit = () => {
    setIsEditing(!isEditing);
  };

  const handleSave = () => {
    console.log(card.cardId)
    console.log("Title ", title)
    updateCard({
      variables: {
        cardId: card.cardId,
        title: title,
        description: description,
        dueDate: dueDate,
      },
    });
    setIsEditing(false);
  };
  
  return (
        <Draggable draggableId={card.cardId} index={index}>
            {(provided) => (
                <div
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                    className="bg-white p-3 rounded shadow mb-2 flex justify-between items-center"
                >
                    {isEditing ? (
                        <div>
                            <input
                                type="text"
                                placeholder="title"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                className="mb-2 pl-2 hover:border hover:border-gray-200 rounded-lg"
                            />
                            <textarea
                              value={description}
                              placeholder="description"
                              onChange={(e) => setDescription(e.target.value)}
                              className="mb-2 pl-2 hover:border hover:border-gray-200 rounded-lg"
                            />
                          <input
                            type="text"
                            placeholder="dueDate"
                            value={dueDate}
                            onChange={(e) => setDueDate(e.target.value)}
                            className="mb-2 pl-2 hover:border hover:border-gray-200 rounded-lg"
                          />
                          <button onClick={handleSave} className="text-blue-500 hover:text-blue-700">
                            Save
                          </button>
                        </div>
                        ) : (
                          <div>
                            <h3 className="font-bold text-sm">{title}</h3>
                            <p className="text-xs">{description}</p>
                          </div>
                    )}
                  <div>
                    <button onClick={handleEdit} className="text-green-500 hover:text-green-700 mr-2.5">
                      <EditIcon className="w-4 h-4" />
                    </button>
                    <button onClick={handleDelete} className="text-red-500 hover:text-red-700 mr-1.5 w-5 h-5">
                      ✕
                    </button>
                  </div>
                </div>
                )}
        </Draggable>
        );
}

export default Card;