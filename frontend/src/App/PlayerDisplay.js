import React, { Component } from 'react';


class PlayerDisplay extends Component {
  constructor(props) {
    super(props);
    this.props = props;
  }

  renderDot(color, focus, i) {
    return (
      <div
        key={`dot-${i}`}
        className={`dot ${focus ? 'focus' : ''}`}
        style={{'backgroundColor': color}}
      />
    );
  }

  renderPlayerDots() {
    const { currentPlayer, direction, playerColors, playerNames } = this.props;
    return (
      <div id='dots-container' >
        {playerNames.map((pn, i) => this.renderDot(playerColors[pn], pn === currentPlayer, i))}
        <div className={direction ? ('point ' + (direction === 1 ? 'right' : 'left')) : '' } />
      </div>
    );
  }

  render() {
    const { playerName, playerNames, playerColors, currentPlayer, winner } = this.props;
    const myTurn = playerName === currentPlayer;
    return (
      <div id='player-display' className='rounded-border'>
        {this.renderPlayerDots()}
        <div id='name-display' className={`${myTurn && !winner ? 'my-turn' : ''} rounded-border`} >
          <div
            id='player-name'
            className={`${myTurn ? 'player-focus' : ''}`}
            style={{'color': playerColors[currentPlayer]}}
          >
            {winner ? winner : currentPlayer}
          </div>
        </div>
      </div>
    );
  }
}

export default PlayerDisplay;
