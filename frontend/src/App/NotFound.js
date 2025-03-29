import React from 'react';
import { Link } from 'react-router-dom';
import * as utils from './utils';

const NotFound = () => {
  return (
    <>
      <div className='not-found-container'>
        <nav></nav>
        <img id='zfudge-icon' src={utils.zfudgeIconPath} />
        <h1>
          no.
        </h1>
        <span>
          click anywhere to go away. 👋
        </span>
      </div>
      <Link className='not-found-link' to='/' />
    </>
  );
};

export default NotFound;
