// frontend/src/App.js
// React UI for Azure OpenAI rice price forecasting

import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    oil: 80,
    inflation: 3.5,
    enso: -1.2,
    fertilizer: 650,
    rainfall: 180
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!response.ok) throw new Error('Prediction failed');

      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌾 Rice Price Forecasting</h1>
        <p>Azure OpenAI Fine-Tuned Model</p>
      </header>

      <main className="container">
        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label>Oil Price ($/bbl)</label>
            <input type="number" name="oil" value={formData.oil} onChange={handleChange} step="0.01" required />
          </div>

          <div className="form-group">
            <label>Inflation (%)</label>
            <input type="number" name="inflation" value={formData.inflation} onChange={handleChange} step="0.01" required />
          </div>

          <div className="form-group">
            <label>ENSO Index</label>
            <input type="number" name="enso" value={formData.enso} onChange={handleChange} step="0.01" required />
          </div>

          <div className="form-group">
            <label>Fertilizer ($/mt)</label>
            <input type="number" name="fertilizer" value={formData.fertilizer} onChange={handleChange} step="0.01" required />
          </div>

          <div className="form-group">
            <label>Rainfall (mm)</label>
            <input type="number" name="rainfall" value={formData.rainfall} onChange={handleChange} step="0.01" required />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Predicting...' : 'Get Prediction'}
          </button>
        </form>

        {error && <div className="error">Error: {error}</div>}

        {prediction && (
          <div className="result">
            <h2>Predicted Price: ${prediction.prediction}</h2>
            <p className="prompt">{prediction.prompt}</p>
          </div>
        )}
      </main>

      <footer>
        <p>Powered by Azure OpenAI | Model: gpt-35-turbo-0125 (Fine-Tuned)</p>
      </footer>
    </div>
  );
}

export default App;
