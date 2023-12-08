import React, { useState } from 'react';
import List from './List';
import { DragDropContext, DropResult } from 'react-beautiful-dnd';
import { useQuery, useMutation } from '@apollo/client';
import {ALL_CARDS_QUERY, ALL_LISTS_QUERY} from '../apollo/queries'
import {
    UPDATE_LIST_ITEMS_MUTATION, DELETE_LIST_ITEM_BY_CARD_ID_MUTATION, CREATE_CARD_MUTATION,
    DELETE_CARD_MUTATION, CREATE_LIST_MUTATION, DELETE_LIST_MUTATION
} from '../apollo/mutations'
import {
    List as ListProps
} from '../types/list'
import {
    AllCards as Cards
} from '../types/card'


interface BoardProps {
    propsLists: ListProps[];
}

function Board({ propsLists }: BoardProps) {
    const { loading: cardsLoading, error: cardsError, data: cardsData } = useQuery<Cards>(ALL_CARDS_QUERY);
    
    const [deleteListItemByCardId] = useMutation(DELETE_LIST_ITEM_BY_CARD_ID_MUTATION, {
        refetchQueries: [{ query: ALL_LISTS_QUERY }],
    });

    const [updateListItems] = useMutation(UPDATE_LIST_ITEMS_MUTATION, {
        refetchQueries: [{ query: ALL_CARDS_QUERY }],
    });
    
    const [createCard] = useMutation(CREATE_CARD_MUTATION, {
        refetchQueries: [{ query: ALL_LISTS_QUERY }],
    });
    
    const [createList] = useMutation(CREATE_LIST_MUTATION, {
        refetchQueries: [{ query: ALL_LISTS_QUERY }]
    });
    
    const [deleteCard] = useMutation(DELETE_CARD_MUTATION);
    
    const [deleteList] = useMutation(DELETE_LIST_MUTATION);
    
    const [isCreating, setIsCreating] = useState(false);
    const [cardTitle, setCardTitle] = useState("")
    const [cardDescription, setCardDescription] = useState("")
    const [cardListName, setCardListName] = useState(propsLists[0].name)
    
    const [listName, setListName] = useState("")

    const [lists, setLists] = useState(propsLists);
    
    // Handle new card form submission
    const handleNewCardSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        createCard({
            variables: {
                title: cardTitle,
                description: cardDescription,
                listName: cardListName,
            },
        }).then((response) => {
            const cardId = response.data.createCard.card.cardId;
            const updatedLists = lists.map(list => {
                if (list.name === cardListName) {
                    const newItems = [...list.items, cardId];
                    return { ...list, items: newItems };
                }
                return list;
            });
            
            const updatedItems = [...updatedLists.filter(list => list.name === cardListName)[0].items]
            setLists(updatedLists);
            handleUpdateListItems(cardListName, updatedItems);

            setCardTitle('');
            setCardDescription('');
            setCardListName(lists[0].name);
        }).catch(error => {
            console.error("Error creating new card", error);
        });
    };
    
    const handleNewListSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        createList({
            variables: {
                name: listName,
            },
        }).then((response => {
            const newLists = [...lists, response.data.createList.list]
            setLists(newLists)
            setListName("")
        })).catch(error => {
            console.error("Error creating new list", error)
        })
    }
    
    const handleCreating = () => {
        setIsCreating(!isCreating);
    };
    
    const handleDeleteList = (name: string) => {
        deleteList({
            variables: { name }
        })
        .then(() => {
            const updatedLists = lists.filter(list => list.name !== name)
            setLists(updatedLists)
        })
    }
    
    const handleDeleteCard = (cardId: string) => {
        deleteCard({
            variables: { cardId }
        })
        .then(() => {
            const updatedLists = lists.map(list => {
                if (list.items.includes(cardId)) {
                    const updatedItems = list.items.filter(item => item !== cardId)
                    return {...list, items: updatedItems}
                }
                return list
            })
            setLists(updatedLists)
        }
        )
    };
    
    
    // Handle deletion of list item
    const handleDeleteListItem = (listName: string, cardId: string) => {
        deleteListItemByCardId({
            variables: { listName, cardId }
        }).then(() => {
            
        })
        .catch(error => {
            // Handle any errors here
            console.error("Error deleting list item:", error);
        });
    };

    // Handle updating list items
    const handleUpdateListItems = (listName: string, items: string[]) => {
        updateListItems({ variables: { listName, items } })
            .then(response => {
                console.log("List items updated successfully", response);
            })
            .catch(error => {
            // Handle error
                console.error("Error updating list items", error);
            });
    };

    // Handle drag end event
    const onDragEnd = (result: DropResult) => {
        const { draggableId, source, destination } = result;

        if (!destination || (source.droppableId === destination.droppableId && source.index === destination.index)) {
            return;
        }
        
        let updatedItems: string[] = [];
        let updatedLists = [...lists]
        
        if (destination.droppableId === source.droppableId) {
            // If the item is moved within the same list
            updatedLists = lists.map(list => {
                if (list.name === destination.droppableId) {
                    updatedItems = [...list.items].filter(item => item !== draggableId);
                    updatedItems.splice(destination.index, 0, draggableId); // Insert at new position
                    return {...list, items: updatedItems };
                } else {
                    return list;
                }
            });
        } else {
            handleDeleteListItem(source.droppableId, draggableId)
            // If the item is moved to a different list
            updatedLists = lists.map(list => {
                if (list.name === source.droppableId) {
                    // Remove the cardId from the source list
                    const newSourceItems = list.items.filter(item => item !== draggableId);
                    return { ...list, items: newSourceItems };
                } else if (list.name === destination.droppableId) {
                    // Add the cardId to the destination list
                    updatedItems = [...list.items];
                    updatedItems.splice(destination.index, 0, draggableId);
                    return { ...list, items: updatedItems };
                } else {
                    // Return the list as is if it's not affected
                    return list;
                }
            });
        }
        setLists(updatedLists)
        handleUpdateListItems(destination.droppableId, updatedItems)
        
       
    };
    
    // Render loading or error states
    if (cardsLoading) return <p>Loading...</p>;
    if (cardsError) return <p>Error: {cardsError.message}</p>;
    if (!cardsData) return null;

    // Function to get cards by list name
    const cardsByListName = (list: ListProps) => {
        let result = []
        for (const item of list.items) {
            const foundCard = cardsData.allCards.find(card => card.cardId === item);

            if (foundCard) {
                result.push(foundCard)
            }
        }
        return result
    }
    
    return (
            <>
            {isCreating ? (
                <div className="flex flex-col justify-around items-center w-full h-screen">
                    <div className="flex w-1/1">
                        <form onSubmit={handleNewCardSubmit} className="m-20">
                            <p className="pb-3.5">Create Card</p>
                            <input
                                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500
                                        block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white
                                        dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-2 mb-2"
                                type="text"
                                value={cardTitle}
                                onChange={(e) => setCardTitle(e.target.value)}
                                placeholder="Card Title"
                            />
                            <textarea
                                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500
                                        block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white
                                        dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-2 mb-2"
                                value={cardDescription}
                                onChange={(e) => setCardDescription(e.target.value)}
                                placeholder="Card Description"
                            />
                            <select
                                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500
                                        block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white
                                        dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-2 mb-2"
                                value={cardListName}
                                onChange={(e) => setCardListName(e.target.value)}
                                >
                                {lists.map(list => (
                                    <option key={list.name} value={list.name}>{list.name}</option>
                                    ))}
                            </select>
                            <button
                                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500
                                        block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white
                                        dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-3 mb-3 pb-3 pt-3"
                                type="submit"
                                >
                                Add Card
                            </button>
                        </form>
                        <form onSubmit={handleNewListSubmit} className="flex flex-col justify-between m-20">
                            <p className="pb-3.5">Create List</p>
                            <input
                                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500
                                        block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white
                                        dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-2 mb-2"
                                type="text"
                                value={listName}
                                onChange={(e) => setListName(e.target.value)}
                                placeholder="List name"
                            />
                            <button
                                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500
                                        block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white
                                        dark:focus:ring-blue-500 dark:focus:border-blue-500 mt-3 mb-3 pb-3 pt-3"
                                type="submit"
                                >
                                Add List
                            </button>
                        </form>
                    </div>
                    <button onClick={handleCreating} className="self-center mr-2.5 bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded mt-4 mb-8">
                        Close
                    </button>
                </div>
            ) : (
                <div className="flex flex-col justify-around items-center w-full h-full">
                        <DragDropContext onDragEnd={onDragEnd}>
                            <div className="flex space-x-4 p-4 overflow-x-auto w-full px-10">
                                {Object.values(lists).map(list => (
                                    <div>
                                        <List key={list.name} listName={list.name} cards={cardsByListName(list)} onDeleteList={handleDeleteList} onDeleteCard={handleDeleteCard}/>
                                    </div>
                                    ))}
                            </div>
                        </DragDropContext>
                    <div>
                        <button onClick={handleCreating} className="self-center mr-2.5 bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded mt-4 mb-8">
                            <span className="inline-block mr-2">+</span>
                            Add
                        </button>
                    </div>
                </div>
            )}
          </> 
        );
}

export default Board;
