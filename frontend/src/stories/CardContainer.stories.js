import { fn } from '@storybook/test';

import CardContainer from '../App/Cards/CardContainer';

export default {
  title: 'CardContainer',
  component: CardContainer,
  tags: ['autodocs'],
  argTypes: {
    backgroundColor: { control: 'color' },
  },
  args: { onClick: fn() },
};

export const Default = {
  args: {
    myCards: true,
    cards: [
      'y1',
      'r6',
      'g+2',
      'br',
      'bs',
      'w',
      'w+4',
    ],
  },
};
