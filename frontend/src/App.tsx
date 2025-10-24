// src/App.tsx
// Full path: /frontend/src/App.tsx

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

interface QueryResponse {
  question: string;
  answer: string;
  sources: number;
}

function App() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError('');
    setResponse(null);

    try {
      const result = await axios.post(`${API_URL}/query`, {
        question: question.trim()
      });
      setResponse(result.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get answer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Enterprise Document Q&A</h1>
        <p>Ask questions about travel itineraries and packages</p>
      </header>

      <main className="App-main">
        <form onSubmit={handleSubmit} className="query-form">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about the documents..."
            disabled={loading}
            className="query-input"
          />
          <button type="submit" disabled={loading} className="query-button">
            {loading ? 'Searching...' : 'Ask'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {response && (
          <div className="response-container">
            <div className="question-box">
              <strong>Question:</strong> {response.question}
            </div>
            <div className="answer-box">
              <strong>Answer:</strong>
              <p>{response.answer}</p>
              <small className="sources-info">
                Based on {response.sources} source{response.sources !== 1 ? 's' : ''}
              </small>
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by Azure OpenAI & Cognitive Search</p>
      </footer>
    </div>
  );
}

export default App;
