import React, { Component } from 'react';


const MAX_LENGTH = process.env.MAX_NAME_LENGTH;;


class PlayerNameInput extends Component {
  constructor(props) {
    super(props);
    this.props = props;
    this.playerNameChange = this.playerNameChange.bind(this);
  }

  playerNameChange(event) {
    const { playerNameChange } = this.props;
    const playerName = event.target.value.slice(0, MAX_LENGTH);
    playerNameChange(playerName);
  }

  render() {
    let { playerName } = this.props;
    // value prop on input should not be null
    if (!playerName) playerName = '';

    return (
      <div className='input-container'>
        <span className='input-title'>Player Name:</span>
        <input
          name='player-name'
          onChange={this.playerNameChange}
          maxLength={MAX_LENGTH}
          placeholder='Player Name'
          value={playerName}
        />
      </div>
    );
  }
}


export default PlayerNameInput;

