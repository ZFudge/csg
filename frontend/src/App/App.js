import React, { Component } from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";

import CreateNewGame from './Forms/CreateNewGame';
import DefaultForm from './Forms/DefaultForm';
import JoinGame from './Forms/JoinGame';
import Game from './Game';
import NotFound from './NotFound';

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          <Routes>
            <Route path="/new" element={<CreateNewGame />} />
            <Route path="/join/:game_hash" element={<JoinGame />} />
            <Route path="/join" element={<JoinGame />} />
            <Route path="/game" element={<Game />} />
            <Route path="/" element={<DefaultForm />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
