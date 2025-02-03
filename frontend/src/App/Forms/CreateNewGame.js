import React, { Component } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { FaHandPointRight } from '@react-icons/all-files/fa/FaHandPointRight';

import PlayerNameInput from './PlayerNameInput';
import ExistingGameLink from './ExistingGameLink';
import './Forms.css';
import * as utils from '../utils';

import webSocket from '../webSocket';

import { withRouter } from '../../utils';

class CreateNewGame extends Component {
  constructor(props) {
    super(props);
    this.props = props;
    this.state = {
      'playerNames': null,
      'playerName': null,
      'playerColors': [],
      'gameHash': null,
      'playerHash': null,
      'createRequestSent': null,
      'startRequestSent': null,
      'copied': null,
      'error': null,
      'redirect': null,
    };
    this.handleSocketData = this.handleSocketData.bind(this);
    this.playerNameChange = this.playerNameChange.bind(this);
    this.createGame = this.createGame.bind(this);
    this.startGame = this.startGame.bind(this);
    this.copyGameHash = this.copyGameHash.bind(this);
  }

  playerNameChange(playerName) {
    this.setState({ playerName });
  }

  copyGameHash() {
    /* Set value of game hash textarea element to a join_game URL with gameHash param. Select the
       element, copy the URL, then restore the original value. If this causes problems it might be
       better to store the URL in a hidden/high opacity w/ absolute position textarea element when
       the game hash is first received, then copy from that. */
    const { gameHash } = this.state;
    const url = location.origin + '/join/' + gameHash;
    const gameHashTextArea = document.querySelector("#game-hash");
    gameHashTextArea.value = url;
    gameHashTextArea.select();
    document.execCommand("copy");
    gameHashTextArea.value = gameHash;
    this.setState({ copied: true });
    setTimeout(() => {
      this.setState({ copied: false });
    }, 3000);
  }

  handleSocketData(socketData) {
    console.log(`socket.on('${this.state.gameHash}'): ${JSON.stringify(socketData)}`)
    const { playerNames, playerColors } = socketData;
    if (playerNames) {
      this.setState({ playerNames, playerColors });
    }
  }

  createGame(e) {
    e.preventDefault();
    const { playerName, createRequestSent } = this.state;
    console.log(`createGame createRequestSent: ${createRequestSent}`);
    if (!playerName || createRequestSent) return;
    // prevent duplicate request to the back end
    this.setState({ createRequestSent: true });
    // used for form data
    localStorage.setItem('player_name', playerName);

    utils.fetchHandler(
      'create_new_game',
      { 'player_name': playerName },
      data => {
        const { gameHash, playerHash, playerNames, playerColors, error } = data;
        if (error) {
          this.setState({ error });
        }
        if (gameHash && playerNames) {
          this.setState({ gameHash, playerHash, playerNames, playerColors });
          webSocket.connect();
          webSocket.socket.on(gameHash, this.handleSocketData);
        }
      }
    );
  }

  startGame() {
    const { gameHash, playerName, playerHash, startRequestSent } = this.state;
    if (startRequestSent) return;
    // prevent duplicate request to the back end
    this.setState({ startRequestSent: true });

    localStorage.setItem('game_data', `${gameHash}___${playerName}___${playerHash}`);

    utils.fetchHandler(
      'start_game',
      {
        'game_hash': gameHash,
        'player_name': playerName,
        'player_hash': playerHash,
      },
      data => {
        console.log(`/start_game data: ${JSON.stringify(data)}`);
        const { playersData, error } = data;

        if (error) {
          this.setState({ error });
        }
        if (playersData) {
          this.setState({ redirect: "/game" });
        }
      }
    );
  }

  componentDidMount() {
    const playerName = localStorage.getItem('player_name');
    if (playerName) this.setState({ playerName });
  }

  componentWillUnmount() {
    const { gameHash } = this.state;
    webSocket.socket.off(gameHash);
  }

  render() {
    const { gameHash, playerName, playerNames, playerColors, copied, error, redirect } = this.state;
    if (redirect) {
      return <Navigate to={redirect} />
    }

    return (
      <>
        <nav>
          <Link to='/' className='link'>Back</Link>
        </nav>
        <img id='zfudge-icon' src={utils.zfudgeIconPath} />
        <div className='align-center'>
          {
            gameHash ? (
              <>
                <h1>Waiting for players to join...</h1>
                <div className='left-aligned'>
                  <div id='game-hash-container'>
                    <div id='game-hash-instructions'>
                      <div>
                        <div>
                          Click this to copy the URL to your clipboard!
                        </div>
                        <div>
                          Then send it to your friends!
                        </div>
                      </div>
                      <FaHandPointRight />
                    </div>
                    <div>
                      <textarea id='game-hash' value={gameHash} readOnly onClick={this.copyGameHash}></textarea>
                      {copied && <div id='copied'>Copied!</div>}
                    </div>
                  </div>
                  {utils.playersList(playerColors)}
                  <button
                    type='button'
                    name='start-game'
                    onClick={this.startGame}
                    disabled={playerNames.length < 2}
                    className={playerNames.length < 2 ? 'disabled' : ''}
                  >
                    Start Game
                  </button>
                </div>
              </>
            ) : (
              <>
                <h1>Create a New Game</h1>
                <form className='left-aligned' onSubmit={this.createGame}>
                  <div>
                    <PlayerNameInput
                      playerNameChange={this.playerNameChange}
                      playerName={playerName}
                    />
                  </div>
                  <button
                    type='submit'
                    name='create-game'
                    disabled={!playerName}
                    className={!playerName ? 'disabled' : ''}
                  >
                    Create Game
                  </button>
                </form>
              </>
            )
          }
          {utils.errorDisplay(error)}
        </div>
        <ExistingGameLink />
      </>
    );
  }
}

export default withRouter(CreateNewGame);

