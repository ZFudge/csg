import React, { Component } from 'react';
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";

import CreateNewGame from './Forms/CreateNewGame';
import JoinGame from './Forms/JoinGame';
import Game from './Game';
import DefaultForm from './Forms/DefaultForm';


class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          {/* A <Switch> looks through its children <Route>s and
              renders the first one that matches the current URL. */}
          <Switch>
            <Route path="/new_game">
              <CreateNewGame />
            </Route>
            <Route path="/join_game">
              <JoinGame />
            </Route>
            <Route path="/game">
              <Game />
            </Route>
            <Route
              path={
                `/(${process.env.REACT_APP_GAME_HASH_REGEX}` +
                  `{${process.env.REACT_APP_GAME_HASH_LENGTH}})`
              }
              exact={false}
              strict={false}
              sensitive={false}
              render={(props) => <JoinGame {...props} /> }
            />
            <Route path="/">
              <DefaultForm />
            </Route>
          </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;

