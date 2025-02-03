import { fn } from '@storybook/test';

import Card from '../App/Cards/Card';

export default {
  title: 'Card',
  component: Card,
  tags: ['autodocs'],
  argTypes: {
    backgroundColor: { control: 'color' },
  },
  args: { onClick: fn() },
};

export const Default = {
  args: {
    classes: "other-player-card",
  }
};

export const Red1 = {
  args: {
    value: "r1",
  }
};

export const GreenDrawTwo = {
  args: {
    value: "g+2",
  }
};

export const BlueReverse = {
  args: {
    value: "br",
  }
};

export const RedSkip = {
  args: {
    value: "rs",
  }
};

export const YellowSkip = {
  args: {
    value: "ys",
  }
};

export const Wild = {
  args: {
    value: "w",
  }
};

export const WildDrawFour = {
  args: {
    value: "w+4",
  }
};

