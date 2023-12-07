import React from 'react';
import Board from './components/Board';
import { useQuery } from '@apollo/client';
import { ALL_LISTS_QUERY } from './apollo/queries';
import ErrorBoundary from './ErrorBoundary'


function App() {
  const { loading, error, data } = useQuery(ALL_LISTS_QUERY);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return (
    <ErrorBoundary>
      <Board propsLists={data.allLists} />
    </ErrorBoundary>
    );
}

export default App;
