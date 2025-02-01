import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import './Forms.css';
import { cookiePath } from '../utils';

import ExistingGameLink from './ExistingGameLink';


class DefaultForm extends Component {

  render() {
    return (
      <>
        <nav></nav>
        <img id='svg-cookie' src={cookiePath} />
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

