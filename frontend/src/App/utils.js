import React from 'react';


const cookiePath = (process.env.PUBLIC_URL + 'images/cookie_face.svg');


function errorDisplay(error) {
  return error ? (
    <>
      <div id='error' className='align-text-center'>
        {error ? <span>{error}</span> : null}
      </div>
    </>
  ) : null;
}


function playersList(playersColors) {
  /* Displays list of players who have joined a pending game */
  return (
    <>
      <h3 className='player-list'>Players</h3>
      {Object.keys(playersColors).map(name => {
        return <div className='joined-player-name' key={name} style={{color: playersColors[name]}}>{name}</div>
      })}
    </>
  );
}


function rejoinedPlayersList(oldGamePlayers, newGamePlayers, activePlayers, gameCreator, playerColors) {
  /* Displays list of players and whether they've
     rejoined an existing game after the game ended.
     oldGamePlayers: All names from previous game.
     newGamePlayers: oldGamePlayers without any who've declined rejoining.
     activePlayers: Names who've accepted rejoining.
  */
  return (
    <>
      <h3 className='player-list'>Pending Players Joining</h3>
      {
        oldGamePlayers.map(name => {
          const status = activePlayers.includes(name) ?
            'accepted' :
            newGamePlayers.includes(name) ?
            'pending' :
            'rejected';
          return (
            <div className='rejoining-player-name-container' key={`rejoining-${name}`}>
              <span className={`player-rejoin-status ${status}`} />
              <span className={gameCreator === name ? 'game-creator' : ''} style={{'color':playerColors[name]}}>{name}</span>
            </div>
          )
        })
      }
    </>
  );
}


function fetchHandler(endpoint, postData, callback) {
  fetch(`/${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(postData),
  })
  .then(res => res.json())
  .then(data => callback(data))
  .catch(console.log);
}


function getGameData({gameHash, playerName, playerHash}, callback) {
  fetch(`/get_game_data?game_hash=${gameHash}&player_name=${playerName}&player_hash=${playerHash}`)
  .then(res => res.json())
  .then(data => callback(data))
  .catch(console.log);
}


function getRandomRotationDegrees() {
  const randomFloat = Math.random();
  return randomFloat < 0.33 ? -360 : randomFloat < 0.66 ? 0 : 360;
}


export {
  cookiePath,
  errorDisplay,
  playersList,
  rejoinedPlayersList,
  fetchHandler,
  getGameData,
  getRandomRotationDegrees,
};

