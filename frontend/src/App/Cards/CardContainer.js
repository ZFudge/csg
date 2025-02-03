import React, { Component } from 'react';

import './Cards.css';

import Card from './Card';

const OTHER_CARD_EM_SPACING = 1.5;


class CardContainer extends Component {
  constructor(props) {
    super(props);
    this.props = props;
  }

  render() {
    const {
      click,
      cards,
      name,
      myCards,
      disabled,
      drawCount,
      deckXYOffsets,
      pileXYOffsets,
      validateCardClickable,
      disableInput,
      enableInput,
      setOuterContainerWidth,
      currentPlayer,
    } = this.props;
    let { classes } = this.props;

    const unoContainer = cards.length === 1 ?
      myCards ? ' my-uno-container' : ' other-uno-container' : '';
    const unoCard = unoContainer ?
      myCards ? ' my-uno-card' : ' other-uno-card' : '';
    classes += unoContainer;
    const drawThreshold = cards.length - drawCount;
    const lastCardIndex = cards.length - 1;

    return (
      <div
        className={`card-container ${classes}`}
      >
        {cards.map((card, i) => {
          return myCards ? (
            <Card
              key={`${card}-${i}`}
              index={i}
              value={card}
              click={click}
              myCard={myCards}
              disableInput={disableInput}
              enableInput={enableInput}
              classes={`playable-card ${unoCard}`}
              disabled={disabled}
              newCard={name === currentPlayer && i >= drawThreshold}
              validateCardClickable={validateCardClickable}
              deckXYOffsets={deckXYOffsets}
              pileXYOffsets={pileXYOffsets}
              isCurrentPlayer={currentPlayer === name}
            />
          ) : (
            <Card
              key={`${card}-${i}`}
              count={cards.length}
              value={''}
              newCard={name === currentPlayer && i >= drawThreshold}
              classes={`other-player-card ${unoCard}`}
              // units of em spacing between overlapped card edges
              left={i * OTHER_CARD_EM_SPACING}
              enableInput={enableInput}
              rotation={Math.random() * 7 - 3.5}
              deckXYOffsets={deckXYOffsets}
              pileXYOffsets={pileXYOffsets}
              setOuterContainerWidth={
                setOuterContainerWidth && i === lastCardIndex ? setOuterContainerWidth : null
              }
              isCurrentPlayer={currentPlayer === name}
            />
          );
        })}
      </div>
    );
  }
}

export default CardContainer;

