import React, { useMemo, useState } from 'https://esm.sh/react@18.2.0';
import { createRoot } from 'https://esm.sh/react-dom@18.2.0/client';

const winPatterns = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

const createInitialBoard = () => {
  const fresh = Array(9).fill('');
  fresh[4] = 'X';
  return fresh;
};

const findWinner = (board) => {
  for (const pattern of winPatterns) {
    const [a, b, c] = pattern;
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      return { winner: board[a], line: pattern };
    }
  }
  return { winner: null, line: [] };
};

const getFreeSpaces = (board) => board.flatMap((cell, idx) => (cell ? [] : [idx]));

const computerMove = (board) => {
  const free = getFreeSpaces(board);
  if (!free.length) return board;
  const pick = free[Math.floor(Math.random() * free.length)];
  const next = [...board];
  next[pick] = 'X';
  return next;
};

const StatusBadge = ({ children }) => <span className="badge">{children}</span>;

const Square = ({ value, onClick, highlight, disabled }) => (
  <button
    className={`square ${highlight ? 'win' : ''} ${disabled ? 'disabled' : ''}`}
    onClick={onClick}
    aria-label={value ? `Square with ${value}` : 'Empty square'}
  >
    <span className={value === 'X' ? 'x' : value === 'O' ? 'o' : ''}>{value}</span>
  </button>
);

const StatusPanel = ({ message, thinking }) => (
  <div className="status">
    <div>
      <p className="subtitle">Status</p>
      <h2 style={{ margin: '4px 0 0' }}>{message}</h2>
    </div>
    {thinking ? <StatusBadge>🤖 Computer thinking</StatusBadge> : null}
  </div>
);

const GuidePanel = () => (
  <div className="card">
    <h3 style={{ margin: 0 }}>Tips for winning</h3>
    <p className="subtitle" style={{ marginTop: 6 }}>
      Sharpen your strategy while enjoying the neon-inspired board.
    </p>
    <ul className="list">
      <li>
        <strong>Watch the center:</strong> the computer opens there. Create forks or block
        lines quickly.
      </li>
      <li>
        <strong>Mind the diagonals:</strong> they close faster than you think—use them to
        force a win.
      </li>
      <li>
        <strong>Play for the draw:</strong> when you cannot win, block each fork and fill
        remaining corners.
      </li>
    </ul>
  </div>
);

const App = () => {
  const [board, setBoard] = useState(() => createInitialBoard());
  const [thinking, setThinking] = useState(false);

  const { winner, line } = useMemo(() => findWinner(board), [board]);
  const freeSpaces = useMemo(() => getFreeSpaces(board), [board]);
  const isDraw = !winner && freeSpaces.length === 0;

  const statusMessage = useMemo(() => {
    if (winner === 'O') return 'You won! 🎉';
    if (winner === 'X') return 'The computer won this round.';
    if (isDraw) return "It's a tie!";
    if (thinking) return 'Computer is thinking...';
    return 'Your move: tap any open square to place an O.';
  }, [winner, isDraw, thinking]);

  const resetGame = () => {
    setBoard(createInitialBoard());
    setThinking(false);
  };

  const handleSquareClick = (index) => {
    if (thinking || winner || isDraw) return;
    if (board[index]) return;

    const nextBoard = [...board];
    nextBoard[index] = 'O';
    setBoard(nextBoard);

    const { winner: playerWinner } = findWinner(nextBoard);
    const movesLeft = getFreeSpaces(nextBoard).length;
    if (playerWinner || movesLeft === 0) {
      setThinking(false);
      return;
    }

    setThinking(true);
    setTimeout(() => {
      setBoard((current) => {
        const currentOutcome = findWinner(current);
        if (currentOutcome.winner || getFreeSpaces(current).length === 0) {
          setThinking(false);
          return current;
        }
        const boardAfterComputer = computerMove(current);
        setThinking(false);
        return boardAfterComputer;
      });
    }, 320);
  };

  return (
    <div className="app-shell">
      <div className="hero">
        <div>
          <div className="pill">
            <span aria-hidden>🕹️</span>
            <span>Quick match</span>
          </div>
          <h1>Tic-Tac-Toe</h1>
          <p>You are O. Outsmart the computer's X opening in the center.</p>
        </div>
        <div className="badge">Powered by React</div>
      </div>

      <div className="layout">
        <div className="card">
          <StatusPanel message={statusMessage} thinking={thinking} />

          <div className="board" role="grid" aria-label="Tic Tac Toe board">
            <div className="grid">
              {board.map((value, idx) => (
                <Square
                  key={idx}
                  value={value}
                  onClick={() => handleSquareClick(idx)}
                  highlight={line.includes(idx)}
                  disabled={thinking || !!winner || isDraw}
                />
              ))}
            </div>
          </div>

          <div className="controls">
            <button className="button primary" onClick={resetGame}>
              🔄 Restart match
            </button>
            <button
              className="button secondary"
              onClick={() => alert('Pro tip: corners are your best friends!')}
            >
              💡 Need a hint?
            </button>
          </div>
        </div>

        <GuidePanel />
      </div>

      <p className="footer">Built for quick fun—no installs needed.</p>
    </div>
  );
};

const container = document.getElementById('root');
createRoot(container).render(<App />);
