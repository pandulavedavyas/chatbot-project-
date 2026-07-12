import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ChatProvider } from './context/ChatContext';
import Welcome from './pages/Welcome';
import Chat from './pages/Chat';

function App() {
  return (
    <ChatProvider>
      <Router>
        <div className="min-h-screen bg-surface-950">
          <Routes>
            <Route path="/" element={<Welcome />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </ChatProvider>
  );
}

export default App;
