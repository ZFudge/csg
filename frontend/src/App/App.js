import React, { Component } from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";

import CreateNewGame from './Forms/CreateNewGame';
import DefaultForm from './Forms/DefaultForm';
import Game from './Game';
import JoinGame from './Forms/JoinGame';


class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          {/* A <Routes> looks through its children <Route>s and
              renders the first one that matches the current URL. */}
          <Routes>
            <Route path="/new_game" element={<CreateNewGame />} />
            <Route path="/join_game" element={<JoinGame />} />
            <Route path="/game" element={<Game />} />
            <Route
              path={
                `/:gameId(${process.env.REACT_APP_GAME_HASH_REGEX}` +
                `{${process.env.REACT_APP_GAME_HASH_LENGTH}})`
              }
              element={<JoinGame />}
            />
            <Route path="/" element={<DefaultForm />} />
          </Routes>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;

