import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import './Forms.css';
import { zfudgeIconPath } from '../utils';

import ExistingGameLink from './ExistingGameLink';


class DefaultForm extends Component {

  render() {
    return (
      <>
        <nav></nav>
        <img id='zfudge-icon' src={zfudgeIconPath} />
        <div id='link-options'>
          <div>
            <Link name='new-game' to='/new' className='link'>New Game</Link>
          </div>
          <div>
            <Link name='join-game' to='/join' className='link'>Join Game</Link>
          </div>
          <ExistingGameLink />
        </div>
      </>
    );
  }
}


export default DefaultForm;

