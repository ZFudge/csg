import React, { Component } from 'react';


class Notification extends Component {
  constructor(props) {
    super(props);
    this.props = props;
    this.state = {
      classes: '',
    };
  }

  componentDidMount() {
    setTimeout(() => {
      this.setState({ classes: 'hidden' });
      setTimeout(() => {
        this.props.removeNotification();
      }, 1500);
    }, 2500);
  }

  render() {
    const { player, firstPerson } = this.props;
    const { classes } = this.state;

    return (
      <div className={`notification ${classes}`}>
        <div className=''>
          {firstPerson ? 'You' : player} {firstPerson ? 'have' : 'has'} uno!
        </div>
      </div>
    );
  }
}


export default Notification;

