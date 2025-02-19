import { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [context, setContext] = useState([]);

  function getAnswer(data) {
    if (data.answer) {
      return data.answer;
    } else {
      return "No response from the server.";
    }
  }

  function renderContext(contextData) {
    if (!contextData || contextData.length === 0) {
      return <p>No context found in the response.</p>;
    }
    return contextData.map((item) => (
      <div key={item.id} className="context-card">
        <p><strong>ID:</strong> {item.id}</p>
        <p>
          <strong>Source:</strong> {item.metadata?.source}{" "}
          (Row: {item.metadata?.row})
        </p>
        <pre className="context-content">{item.page_content}</pre>
      </div>
    ));
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      });

      const data = await res.json();
      setContext(data.context || []);
      const answer = getAnswer(data);
      setResponse(answer);
    } catch (error) {
      console.error("Error fetching response:", error);
      setResponse("Error occurred while fetching the response.");
    }
  };

  return (
    <div className="App">
      <h1>Teaching Your AI New Tricks</h1>
      <p>Query the AI on yourself or anyone from the knowledge base!</p>

      <div>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            className='query-input'
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your query..."
            
          />
          <button type="submit" className="query-submit-button">
            Submit
          </button>
        </form>
      </div>
      
    
      <div className="data-card">
        <h2>Response</h2>
        <p>{response}</p>
      </div>
      <div className="data-card">
        <h2>Context</h2>
        
        <div className="context-container">
          {renderContext(context)}
        </div>
      </div>
    </div>
  );
}

export default App;
