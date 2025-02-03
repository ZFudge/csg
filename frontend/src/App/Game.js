import React, { Component } from 'react';
import { useNavigate } from 'react-router-dom';

import RecycleGame from './Forms/RecycleGame';
import WildCardColorChoice from './Cards/WildCardColorChoice';
import PlayerContainer from './PlayerContainer';
import Card from './Cards/Card';
import PlayerDisplay from './PlayerDisplay';
import Notification from './Notification';
import { withRouter } from '../utils';
import * as utils from './utils';
import webSocket from './webSocket';

class Game extends Component {
  constructor(props) {
    super(props);
    this.props = props;
    this.state = {
      gameHash: '',
      cardType: '',
      cardColor: '',
      myCards: [],
      playerName: '',
      playerHash: '',
      players: {},
      playerColors: [],
      currentPlayer: '',
      playerOrder: [],
      increment: null,
      error: '',
      winner: '',
      displayWildCardColorChoice: false,
      drawCount: 0,
      pendingDrawCount: 0,
      deckX: null,
      deckY: null,
      pileX: null,
      pileY: null,
      overlay: false,
      playerHasUno: '',
    };
    this.handleGameSocketData = this.handleGameSocketData.bind(this);
    this.validateCardClickable = this.validateCardClickable.bind(this);
    this.playCard = this.playCard.bind(this);
    this.drawCard = this.drawCard.bind(this);
    this.sortCards = this.sortCards.bind(this);
    this.disableInput = this.disableInput.bind(this);
    this.enableInput = this.enableInput.bind(this);
    this.setOffsets = this.setOffsets.bind(this);
    this.loadGame = this.loadGame.bind(this);
    this.setUnoNone = this.setUnoNone.bind(this);
    this.setError = this.setError.bind(this);
  }

  setUnoNone() {
    this.setState({ playerHasUno: '' });
  }

  disableInput() {
    this.setState({ overlay: true });
  }

  enableInput() {
    this.setState({ overlay: false });
  }

  waitingForPlayerCard() {
    const { playerName, currentPlayer, displayWildCardColorChoice, winner } = this.state;
    return playerName === currentPlayer && !displayWildCardColorChoice && !winner;
  }

  cardIsValid(color, type) {
    const { cardColor, cardType } = this.state;
    return [cardColor, 'w'].includes(color) || cardType === type;
  }

  handleGameSocketData(socketData) {
    const {
      players,
      cardType,
      cardColor,
      currentPlayer,
      active,
      winner,
      increment,
      drawCount,
      playerHasUno,
    } = socketData;
    const { playerName, pendingDrawCount } = this.state;
    const myTurn = playerName === currentPlayer;
    const updatedData = {
      cardType: cardType !== 'w' ? cardType : '',
      displayWildCardColorChoice: cardColor === 'w' && myTurn && !winner,
    };

    if (this.state.drawCount) {
      updatedData.drawCount = 0;
    }
    if (drawCount) {
      if ((myTurn && !updatedData.displayWildCardColorChoice) || (!myTurn && cardColor !== 'w')) {
        // current player draws one card from deck OR previous player played a +2
        updatedData.drawCount = drawCount;
      } else {
        // current player is choosing +4 wild card color
        updatedData.pendingDrawCount = drawCount;
      }
    } else if (pendingDrawCount) {
      // previous player chose +4 wild card color
      // between choosing wild card and choosing the color no socket broadcasts are made
      updatedData.drawCount = pendingDrawCount;
      updatedData.pendingDrawCount = 0;
    }

    if (increment) updatedData.increment = increment;
    if (players) {
      updatedData.players = players;
      updatedData.myCards = players[playerName];
    }
    if (playerHasUno) updatedData.playerHasUno = playerHasUno;
    if (cardColor) updatedData.cardColor = cardColor;
    if (currentPlayer) updatedData.currentPlayer = currentPlayer;
    if (Object.keys(updatedData).length) this.setState(updatedData);
    if (!active && winner) {
      const { gameHash } = this.state;
      webSocket.socket.off(gameHash);
      this.setState({ winner });
    }
  }

  sortCards() {
    const { gameHash, playerName, playerHash, drawCount } = this.state;
    if (drawCount) this.setState({ drawCount: 0 });

    utils.fetchHandler(
      'sort_cards',
      {
        'game_hash': gameHash,
        'player_name': playerName,
        'player_hash': playerHash,
      },
      data => {
        const { error, myCards } = data;
        if (error) return this.setState({ error });
        this.setState({ myCards });
      }
    );
  }

  drawCard() {
    const { gameHash, playerName, playerHash, drawCount } = this.state;
    if (this.waitingForPlayerCard()) {
      utils.fetchHandler(
        'draw_cards',
        {
          'game_hash': gameHash,
          'player_name': playerName,
          'player_hash': playerHash,
        },
        data => {
          const { error } = data;
          if (error) {
            return this.setState({ error });
          }
        }
      );
    }
  }

  validateCardClickable(color, type) {
    return this.cardIsValid(color, type) && this.waitingForPlayerCard();
  }

  playCard(color, type, index) {
    if (this.cardIsValid(color, type) && this.waitingForPlayerCard()) {
      const {
        gameHash,
        playerName,
        playerHash,
        myCards,
        drawCount,
      } = this.state;

      utils.fetchHandler(
        'play_card',
        {
          color,
          type,
          index,
          'game_hash': gameHash,
          'player_name': playerName,
          'player_hash': playerHash,
        },
        data => {
          const { error } = data;
          if (error) this.setState({ error });
        }
      );
    } else {console.log(`playCard cannot play`);}
  }

  loadGame(data, gameHash, playerName, playerHash) {
    const { gameData, error } = data;
    if (error) {
      this.setState({ error });
    } else if (gameData) {
      const {
        players,
        card_type,
        card_color,
        current_player,
        player_order,
        player_increment,
        player_colors,
      } = gameData;

      this.setState({
        gameHash,
        playerName,
        playerHash,
        players,
        playerColors: player_colors,
        cardType: card_type === 'w' ? '' : card_type,
        cardColor: card_color,
        currentPlayer: current_player,
        playerOrder: player_order,
        increment: player_increment,
        myCards: players[playerName],
        displayWildCardColorChoice: (
          ['w', '+4'].includes(card_type) &&
          card_color === 'w' &&
          playerName === current_player
        ),
      });

      webSocket.connect();
      webSocket.socket.on(gameHash, this.handleGameSocketData);
    }
  }

  setOffsets(x, y, deck) {
    if (deck) return this.setState({ deckX: x, deckY: y });
    this.setState({ pileX: x, pileY: y });
  }

  componentDidMount() {
    const localGameData = localStorage.getItem('game_data');
    if (localGameData) {
      const [ gameHash, playerName, playerHash ] = localGameData.split('___');
      utils.getGameData(
        {
          gameHash,
          playerName,
          playerHash,
        },
        data => this.loadGame(data, gameHash, playerName, playerHash)
      );
    } else {
      // no active game, redirect to home page
      const navigate = useNavigate();
      navigate("/");
    }
  }

  setError(error) {
    this.setState({ error });
  }

  render() {
    const {
      gameHash,
      playerName,
      playerHash,
      players,
      playerColors,
      playerOrder,
      myCards,
      cardType,
      cardColor,
      currentPlayer,
      winner,
      displayWildCardColorChoice,
      error,
      increment,
      deckX,
      deckY,
      pileX,
      pileY,
      drawCount,
      overlay,
      playerHasUno,
    } = this.state;

    if (!gameHash && !playerName) {
      return (
        <>
          <span>Loading</span>
          {utils.errorDisplay(error)}
        </>
      );
    }

    // always keep the player's own cards at top
    const playerNamesCardsOrder = [];
    // display names in consistent order regardless of pov
    const playerNamesDisplayOrder = [];
    playerOrder.map(p => {
      playerNamesDisplayOrder.push(p[0]);
      p[0] === playerName ? playerNamesCardsOrder.unshift(p[0]) : playerNamesCardsOrder.push(p[0]);
    });

    const disabled = !this.waitingForPlayerCard();
    return (
      <>
        {/* Trigger a transparent, click-blocking overlay if currently running card animations. */}
        {overlay && <div id='overlay'></div>}

        {/* Trigger notification for all players when a player has an uno. */}
        {
          playerHasUno ?
            <Notification
              player={playerHasUno}
              firstPerson={playerHasUno === playerName}
              removeNotification={this.setUnoNone}
            /> :
            null
        }

        {/* Trigger modal for starting/declining a new game. */}
        {
          winner ?
            <RecycleGame
              winner={winner}
              gameHash={gameHash}
              playerName={playerName}
              playerHash={playerHash}
              playerColors={playerColors}
              oldGamePlayers={playerNamesDisplayOrder}
              history={this.props.history}
              setError={this.setError}
              webSocket={webSocket}
            /> :
            null
        }

        {/* Display current player in play */}
        <PlayerDisplay
          playerNames={playerNamesDisplayOrder}
          playerName={playerName}
          currentPlayer={currentPlayer}
          winner={winner}
          direction={playerOrder.length > 2 ? increment : 0}
          playerColors={playerColors}
        />

        {/* Deck and pile of played cards */}
        <div className='card-container'>
          <Card
            click={this.drawCard}
            deck={true}
            classes='deck'
            color=''
            disabled={disabled}
            setOffsets={this.setOffsets}
            disableInput={this.disableInput}
            isCurrentPlayer={playerName === currentPlayer}
          />
          <Card
            color={cardColor}
            type={cardType}
            pile={true}
            classes={'pile'}
            setOffsets={this.setOffsets}
          />
          {displayWildCardColorChoice ?
            <WildCardColorChoice
              gameHash={gameHash}
              playerName={playerName}
              playerHash={playerHash}
              setError={this.setError}
            /> :
            null
          }
        </div>

        {/* Display all player card hands */}
        {
          playerNamesCardsOrder.map((name, i) => {
            const isMe = name === playerName;
            return (
              <PlayerContainer
                key={name}
                name={name}
                color={playerColors[name]}
                cards={isMe ? myCards : players[name]}
                me={isMe}
                nameClick={isMe ? this.sortCards : null}
                cardClick={isMe ? this.playCard : null}
                disabled={disabled}
                disableInput={isMe ? this.disableInput : null}
                enableInput={this.enableInput}
                validateCardClickable={isMe ? this.validateCardClickable : null}
                drawCount={drawCount}
                currentPlayer={currentPlayer}
                pileXYOffsets={[ pileX, pileY ]}
                deckXYOffsets={[ deckX, deckY ]}
              />
            );
          })
        }

        {utils.errorDisplay(error)}
      </>
    );
  }
}

export default withRouter(Game);

