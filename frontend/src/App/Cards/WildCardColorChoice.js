import React, { Component } from 'react';

import './Cards.css';

import { fetchHandler } from '../utils';


const COLORS = ['r', 'g', 'b', 'y'];


class WildCardColorChoice extends Component {
  constructor(props) {
    super(props);
    this.props = props;
    this.state = {};

    this.setColor = this.setColor.bind(this);
  }

  setColor() {
    const { gameHash, playerName, playerHash } = this.props;
    const color = event.target.value;

    fetchHandler(
      'set_color',
      {
        color,
        'game_hash': gameHash,
        'player_name': playerName,
        'player_hash': playerHash,
      },
      (data) => {
        console.log(`/set_color resp: ${JSON.stringify(data)}`);
        const { error } = data;
        if (error) this.props.setError(error);
      }
    );
  }

  renderButton(color) {
    return (
      <button
        key={`${color}`}
        value={`${color}`}
        className={`${color} color-choice keep-color`}
        onClick={this.setColor}
        type='button'
      >
      </button>
    );
  }

  render() {
    return (
      <div className='color-choice-container'>
        {COLORS.map(color => this.renderButton(color))}
      </div>
    );
  }
}

export default WildCardColorChoice;

