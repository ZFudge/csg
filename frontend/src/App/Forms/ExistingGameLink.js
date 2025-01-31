import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import './Forms.css';

import { getGameData } from '../utils';


class ExistingGameLink extends Component {
  constructor(props) {
    super(props);
    this.state = {
      'activeGame': false,
    };
  }

  componentDidMount() {
    const localGameData = localStorage.getItem('game_data');
    console.log(`localGameData: ${JSON.stringify(localGameData)}`);

    if (localGameData) {
      const [ gameHash, playerName, playerHash ] = localGameData.split('___');
      getGameData(
        {
          gameHash,
          playerName,
          playerHash,
        },
        data => {
          console.log(`data: ${JSON.stringify(data)}`);
          const { error, gameData } = data;
          if (error) {
            localStorage.removeItem('game_data');
          } else if (gameData && gameData.active) {
            this.setState({ 'activeGame': true });
          }
        }
      );
    }
  }

  render() {
    const { activeGame } = this.state;
    if (activeGame) {
      return (
        <div>
          <Link to='/game' className='link'>Rejoin Game</Link>
        </div>
      );
    }
    return (<></>);
  }
}


export default ExistingGameLink;

