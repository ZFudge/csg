import React, { Component } from 'react';

import CardContainer from './Cards/CardContainer';


class PlayerContainer extends Component {
  constructor(props) {
    super(props);
    this.props = props;
    this.state = {
      width: null,
    }
    this.setWidth = this.setWidth.bind(this);
  }

  setWidth(width) {
    this.setState({ width });
  }

  render() {
    const {
      name,
      color,
      me,
      nameClick,
      cardClick,
    } = this.props;
    const { width } = this.state;

    return (
      <div
        style={{ width: `${width}em`, color: color }}
        className={me ? '' : 'other-player-outer-card-container'}
      >
        <div
          onClick={nameClick}
          className={'players-name-cards' + (me ? ' pointer' : '')}
        >
          {name}
        </div>
        <CardContainer
          {...this.props}
          myCards={me}
          classes={me ? 'mine' : 'not-mine'}
          setOuterContainerWidth={me ? null : this.setWidth}
          click={cardClick}
        />
      </div>
    );
  }
}

export default PlayerContainer;
