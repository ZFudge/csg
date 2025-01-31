import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import './Forms.css';

import { getGameData, rejoinedPlayersList, fetchHandler } from '../utils';


class RecycleGame extends Component {
  constructor(props) {
    super(props);
    this.state = {
      // Excludes exited players. All names from previous game in this.props.playerNames
      playerHash: null,
      newGamePlayers: [],
      activePlayers: [],
      pending: true,
      active: false,
      gameCreator: '',
      abort: null,
    };
    this.receiveSocketData = this.receiveSocketData.bind(this);
    this.createRecycledGame = this.createRecycledGame.bind(this);
    this.joinRecycledGame = this.joinRecycledGame.bind(this);
    this.startGame = this.startGame.bind(this);
    this.accept = this.accept.bind(this);
    this.declineAndexit = this.declineAndexit.bind(this);
  }

  receiveSocketData(socketData) {
    const { playerName } = this.props;
    const { activePlayers, newGamePlayers, gameCreator } = this.state;
    const {
      error,
      active,
      playerNames,
      activatedPlayer,
      // only returned by /create_new_game.
      setGameCreator,
      // only returned by /exit.
      abort,
    } = socketData;

    if (active) {
      window.location.reload();
      return;
    } else if (abort) {
      localStorage.removeItem('game_data');
    }

    if (activatedPlayer && !activePlayers.includes(activatedPlayer)) {
      activePlayers.push(activatedPlayer);
    }

    this.setState({
      newGamePlayers: playerNames || newGamePlayers,
      activePlayers,
      gameCreator: gameCreator || setGameCreator,
      abort,
    });
    if (error) this.props.setError(error);
  }

  createRecycledGame() {
    // any who have declined will be missing from newGamePlayers
    const { newGamePlayers } = this.state;
    const { gameHash, playerName, playerColors } = this.props;
    fetchHandler(
      'create_new_game',
      {
        'game_hash': gameHash,
        'player_name': playerName,
        'player_names': newGamePlayers,
        'recycled_game': true,
        'player_colors': playerColors,
      },
      data => {
        console.log(`/new_game resp data: ${JSON.stringify(data)}`);
        const { playerHash, error } = data;
        if (error) {
          this.props.setError(error);
        } else if (playerHash) {
          // update game_data with new player hash so /game redirect uses the correct hash
          localStorage.setItem('game_data', `${gameHash}___${playerName}___${playerHash}`);
          this.setState({
            playerHash,
            'pending': false,
          });
        }
      }
    );
  }

  joinRecycledGame() {
    const { gameHash, playerName } = this.props;
    fetchHandler(
      'add_player',
      {
        'game_hash': gameHash,
        'player_name': playerName,
        'recycled_game': true,
      },
      data => {
        console.log(`/new_game resp data: ${JSON.stringify(data)}`);
        const { playerHash, error } = data;
        if (error) {
          this.props.setError(error);
        } else if (playerHash) {
          // update game_data with new player hash so /game redirect uses the correct hash
          localStorage.setItem('game_data', `${gameHash}___${playerName}___${playerHash}`);
          this.setState({
            playerHash,
            'pending': false,
          });
        }
      }
    );
  }

  accept() {
    const { activePlayers, } = this.state;
    if (activePlayers.length) {
      this.joinRecycledGame();
    } else {
      this.createRecycledGame();
    }
  }

  declineAndexit() {
    const { gameHash, playerName, playerHash } = this.props;

    fetchHandler(
      'exit',
      {
        'game_hash': gameHash,
        'player_name': playerName,
        'player_hash': playerHash,
      },
      data => {
        console.log(`/exit resp data: ${JSON.stringify(data)}`);
        const { error } = data;
        if (error) this.props.setError(error);
        localStorage.removeItem('game_data');
        this.props.history.push('/');
      }
    );
  }

  startGame() {
    const { gameHash, playerName } = this.props;
    const { playerHash } = this.state;

    fetchHandler(
      'start_game',
      {
        'recycled_game': true,
        'game_hash': gameHash,
        'player_name': playerName,
        'player_hash': playerHash,
      },
      data => {
        console.log(`/start_game resp data: ${JSON.stringify(data)}`);
        const { error } = data;
        if (error) this.props.setError(error);
      }
    );
  }

  componentDidMount() {
    const { oldGamePlayers, webSocket } = this.props;
    this.setState({ newGamePlayers: oldGamePlayers });
    const localGameData = localStorage.getItem('game_data');
    const [ gameHash, playerName, playerHash ] = localGameData.split('___');
    webSocket.connect();
    webSocket.socket.on(`${gameHash}_recycled_game`, this.receiveSocketData);
  }

  componentWillUnmount() {
    const { gameHash, webSocket } = this.props;
    webSocket.socket.off(`${gameHash}_recycled_game`);
  }

  render() {
    const { winner, playerName, playerColors, oldGamePlayers } = this.props;
    const {
      newGamePlayers,
      activePlayers,
      pending,
      gameCreator,
      abort,
    } = this.state;

    return (
      <div id='recycle-game'>
        <div className='modal'>
          {
            pending && !abort ? (
              <>
                <h1>{`${winner} wins!`}</h1>
                <div>Start new game?</div>
                <button type='button' onClick={this.accept}>Yeah!</button>
                <button type='button' onClick={this.declineAndexit}>Na.</button>
              </>
            ) : (
              <>
                <h1>{abort ? 'Not enough players to start a new game' : 'Waiting for start'}</h1>
                <div className='rejoined-player-list-container'>
                  {
                    !pending ?
                      rejoinedPlayersList(
                        oldGamePlayers,
                        newGamePlayers,
                        activePlayers,
                        gameCreator,
                        playerColors
                      ) :
                      null
                  }
                </div>
                {
                  gameCreator === playerName && !abort ?
                    <button
                      type='button'
                      onClick={this.startGame}
                      disabled={activePlayers.length < 2}
                    >
                      Start
                    </button> :
                    abort ?
                      <Link to='/' className='link'>Return to Main Page</Link> :
                      null
                }
              </>
            )
          }
        </div>
      </div>
    );
  }
}


export default RecycleGame;

