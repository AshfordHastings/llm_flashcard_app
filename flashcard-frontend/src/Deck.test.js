import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import DeckList from './DeckList';

jest.mock('axios');

describe('DeckList Component', () => {
  it('fetches and displays decks', async () => {
    axios.get.mockResolvedValue({
      data: {
        value: [{ id: '1', name: 'Test Deck' }],
      },
    });

    render(<DeckList />);
    await waitFor(() => screen.getByText('Test Deck'));

    expect(screen.getByText('Test Deck')).toBeInTheDocument();
  });
});
