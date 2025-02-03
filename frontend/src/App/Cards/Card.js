import React, { Component } from 'react';
import { FaBan } from "@react-icons/all-files/fa/FaBan";
import { FaSyncAlt } from "@react-icons/all-files/fa/FaSyncAlt";

import './Cards.css';
import { getRandomRotationDegrees } from '../utils';

// Should match transition-duration property of card class
const CARD_TRANSITION_MS = 400;
// How long to wait after card has been drawn to enable input
const DRAW_WAIT_MS = 450;


class Card extends Component {
  constructor(props) {
    super(props);
    this.props = props;
    this.myRef = React.createRef();
    this.click = this.click.bind(this);
  }

  getOffsets() {
    const { current } = this.myRef;
    const totalOffsetLeft = current.offsetLeft;
    const totalOffsetTop = current.offsetTop + current.offsetParent.offsetTop;
    return { totalOffsetLeft, totalOffsetTop };
  }

  click(color, type) {
    const { disableInput } = this.props;
    disableInput();
    if ((color && type) || color === 'w') {
      // playCard
      const { current } = this.myRef;
      const [ xPileOffset, yPileOffset ] = this.props.pileXYOffsets;
      const { totalOffsetLeft, totalOffsetTop } = this.getOffsets();
      const yMove = -1 * (totalOffsetTop - yPileOffset - current.offsetTop);
      const yStart = current.offsetTop;

      current.style.left = `${totalOffsetLeft}px`;
      current.style.top = `${yStart}px`;
      current.style.zIndex = 999;
      setTimeout(() => {
        current.style.position = 'absolute';
        current.style.left = `${xPileOffset}px`;
        current.style.top = `${yMove}px`;
        current.style.transform = `rotate(${getRandomRotationDegrees()}deg)`;
        setTimeout(() => {
          this.props.click(color, type, this.props.index);
          this.props.enableInput();
        }, CARD_TRANSITION_MS);
      }, 100);
      return;
    }
    // drawCard
    this.props.click();
  }

  componentDidMount() {
    // only runs on the last card of an other player's cards
    if (this.props.setOuterContainerWidth) {
      const { setOuterContainerWidth, left } = this.props;
      setOuterContainerWidth(left);
    }
    const { deck, pile, setOffsets, newCard } = this.props;
    if (deck || pile) {
      const { totalOffsetLeft, totalOffsetTop } = this.getOffsets();
      if (deck) {
        return setOffsets(totalOffsetLeft, totalOffsetTop, deck);
      }
      setOffsets(totalOffsetLeft, totalOffsetTop);
    } else if (newCard) {
      const { current } = this.myRef;
      const { myCard } = this.props;
      const [ xDeckOffset, yDeckOffset ] = this.props.deckXYOffsets;
      const { totalOffsetLeft, totalOffsetTop } = this.getOffsets();
      const yEnd = current.offsetTop;
      const xEnd = current.offsetLeft;
      const yStart = -1 * (totalOffsetTop - yDeckOffset - current.offsetTop);
      // not sure why opponent card, when rendered with a 'left' style value of ~0px,
      // initially behaves as if its left value is rendered with the value of xEnd.
      // because this only happens when it's the opponent card that's being drawn,
      // counteract this abnormal offset for opponent cards only.
      const xStart = myCard ? xDeckOffset : -xEnd;

      current.style.left = `${xStart}px`;
      current.style.top = `${yStart}px`;
      // Set non-zero rotation value now, then reset it to 0 during the animation. This accomplishes
      // the same effect, but prevents unwanted rotations on subsequent DOM updates caused by
      // the rotation value being reset to 0.
      current.style.transform = `rotate(${getRandomRotationDegrees()}deg)`;
      current.style.zIndex = 999;

      setTimeout(() => {
        current.classList.remove('hidden');
        current.style.position = 'absolute';
        if (myCard) {
          current.style.top = `${yEnd}px`;
        } else {
          current.style.top = `0px`;
        }
        current.style.left = `${xEnd}px`;
        current.style.transform = 'rotate(0deg)';
        setTimeout(() => {
          current.style.transform = '';
          current.style.position = '';
          setTimeout(() => this.props.enableInput(), DRAW_WAIT_MS);
        }, CARD_TRANSITION_MS);
      }, 100);
    }
  }

  render() {
    const {
      value,
      myCard,
      deck,
      left,
      rotation,
      disabled,
      newCard,
      validateCardClickable,
      isCurrentPlayer,
    } = this.props;

    let { color, type, classes } = this.props;
    if (value && !color && !type) {
      color = value[0];
      type = value.slice(1);
      if (type === 'd') type = '+2';
    }

    if (disabled) classes += ' disabled';
    if (newCard) classes += ' hidden';
    if (['6', '9'].includes(type)) classes += ' underline';

    const clickable = !isCurrentPlayer ? null :
      myCard && validateCardClickable ?
      validateCardClickable(color, type) : deck;

    let cornerContent = type;
    let centerContent = type;
    if (centerContent && centerContent.includes('+') || color === 'w') {
      if (color === 'w') {
        if (centerContent.includes('+')) {
          // draw 4
          centerContent = (
            <div className="wild-draw-four">
              <div className="rectangle red"/>
              <div className="rectangle green"/>
              <div className="rectangle blue"/>
              <div className="rectangle yellow"/>
            </div>
          );
        } else {
          // wild
          cornerContent = <div className="wild"/>;
          centerContent = cornerContent;
        }
      } else {
        // draw
        centerContent = (
          <div className="draw">
            <div className="rectangle one"/>
            <div className="rectangle two"/>
          </div>
        );
      }
    } else if (type === 's') {
      // skip
      cornerContent = <FaBan />;
      centerContent = cornerContent;
    } else if (type === 'r') {
      // reverse
      cornerContent = <FaSyncAlt />;
      centerContent = cornerContent;
    }

    return (
      <div
        ref={this.myRef}
        data-value={value}
        className={`card ${color} ${classes}`}
        onClick={
          !clickable ? null : myCard ? () => this.click(color, type) :
            deck ? () => this.click() : null
        }
        style={{
          'left': `${left}em`,
          'transform': `rotate(${rotation}deg)`,
        }}
      >
        <div className='corner up-left'>
          <span>{cornerContent}</span>
        </div>
        <div className='center'>
          {centerContent}
        </div>
        <div className='corner dn-right'>
          <span>{cornerContent}</span>
        </div>
      </div>
    );
  }
}

export default Card;
