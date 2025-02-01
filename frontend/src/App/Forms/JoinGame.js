import React, { Component } from 'react';
import { Link, Navigate } from 'react-router-dom';

import PlayerNameInput from './PlayerNameInput';
import ExistingGameLink from './ExistingGameLink';
import './Forms.css';
import { withRouter } from '../../utils';
import * as utils from '../utils';
import webSocket from '../webSocket';


class JoinGame extends Component {
  constructor(props) {
    super(props);
    this.props = props;
    this.state = {
      'playerNames': null,
      'playerColors': [],
      'playerName': '',
      'gameHash': '',
      'playerHash': null,
      'readOnly': false,
      'addPlayerRequestSent': null,
      'error': null,
      'redirect': null,
    };
    this.playerNameChange = this.playerNameChange.bind(this);
    this.gameHashChange = this.gameHashChange.bind(this);
    this.joinGame = this.joinGame.bind(this);
    this.handleSocketData = this.handleSocketData.bind(this);
  }

  handleSocketData(socketData) {
    const { playerNames, playerColors, error, active } = socketData;
    if (active) {
      const { gameHash, playerName, playerHash } = this.state;
      localStorage.setItem('game_data', `${gameHash}___${playerName}___${playerHash}`);
      this.setState({ redirect: "/game" });
    }
    if (error) {
      return this.setState({ error });
    }
    if (playerNames) {
      this.setState({ playerNames, playerColors });
    }
  }

  playerNameChange(playerName) {
    this.setState({ playerName });
  }

  gameHashChange(event) {
    const gameHash = event.target.value;
    this.setState({ gameHash });
  }

  getGameHashFromQueryParam() {
    const path = location.pathname.slice(6);
    if (path === 'join') return;
    // const hashLength = Number(process.env.REACT_APP_GAME_HASH_LENGTH);
    const hashLength = 8;
    if (path.length === hashLength) {
      this.setState({ 'gameHash': path, readOnly: true });
    }
  }

  joinGame(e) {
    e.preventDefault();
    const { gameHash, playerName, redirect, addPlayerRequestSent } = this.state;
    if (!gameHash || !playerName || addPlayerRequestSent) return;
    // prevent duplicate request to the back end
    this.setState({ addPlayerRequestSent: true });
    localStorage.setItem('player_name', playerName);

    utils.fetchHandler(
      'add_player',
      {
        'game_hash': gameHash,
        'player_name': playerName,
      },
      data => {
        const { redirect, playerNames, playerHash, playerColors, error } = data
        if (error) {
          this.setState({ error });
        } else if (redirect) {
          // redirect from submitted form to /game when game is active
          const localGameData = localStorage.getItem('game_data');
          if (localGameData) {
            const [ lSGameHash, lSPlayerName, lSPlayerHash ] = localGameData.split('___');
            const { playerName, gameHash } = this.state;
            if (lSPlayerName === playerName && lSGameHash === gameHash) {
              this.setState({ redirect: "/game" });
            }
          }
        } else if (playerNames) {
          webSocket.connect();
          webSocket.socket.on(gameHash, this.handleSocketData);
          this.setState({ playerHash, playerNames, playerColors });
        }
      }
    );
  }

  componentDidMount() {
    const playerName = localStorage.getItem('player_name');
    if (playerName) this.setState({ playerName });
    this.getGameHashFromQueryParam();
  }

  componentWillUnmount() {
    const { gameHash } = this.state;
    webSocket.socket.off(gameHash);
  }

  render() {
    const { playerName, playerNames, playerColors, error, gameHash, readOnly, redirect } = this.state;
    const activeButton = playerName && gameHash.length === 8;
    if (redirect) {
      return <Navigate to={redirect} />
    }

    return (
      <>
        <nav>
          <Link to='/' className='link'>Back</Link>
        </nav>
        <img id='svg-cookie' src={utils.cookiePath} />
        <div className='align-center'>
          {
            playerNames ?
            (
              <>
                <h1 className='align-center'>Waiting for Game to start</h1>
                <div>
                  <h3>Game: {gameHash}</h3>
                </div>
                {utils.playersList(playerColors)}
              </>
            ) : (
              <>
                <h1 className='align-center'>Join a Game</h1>
                <form className='left-aligned' onSubmit={this.joinGame}>
                  <div>
                    <div className='input-container'>
                      <span className='input-title'>Game Code:</span>
                      <input
                        name='game-hash'
                        placeholder='########'
                        onChange={this.gameHashChange}
                        value={gameHash}
                        readOnly={readOnly}
                      />
                    </div>
                    <PlayerNameInput
                      playerNameChange={this.playerNameChange}
                      playerName={playerName}
                    />
                  </div>
                  <button
                    type='submit'
                    name='join-game'
                    disabled={!activeButton}
                    className={activeButton ? '' : 'disabled'}
                  >
                    Join Game
                  </button>
                  {utils.errorDisplay(error)}
                </form>
              </>
            )
          }
        </div>
        <ExistingGameLink />
      </>
    );
  }
}


export default withRouter(JoinGame);

