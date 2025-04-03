import React, { useState } from "react";
import "./App.css";

const API_URL = "https://lotofacil-api.onrender.com";

function App() {
  const [apostas, setApostas] = useState([]);
  const [origem, setOrigem] = useState("");
  const [erro, setErro] = useState(null);
  const [inputDezenas, setInputDezenas] = useState("");
  const [analise, setAnalise] = useState(null);
  const [historico, setHistorico] = useState([]);
  const [filtro, setFiltro] = useState("");

  const fetchApostas = async (endpoint) => {
    try {
      setErro(null);
      setAnalise(null);
      const response = await fetch(`${API_URL}/${endpoint}`);
      const data = await response.json();

      if (data.apostas || data.aposta) {
        const apostasFormatadas = data.apostas || [data.aposta];
        setApostas(apostasFormatadas);
        setOrigem(data.origem);
      } else {
        setErro("Resposta inesperada da IA");
        setApostas([]);
        setOrigem("");
      }
    } catch (error) {
      setErro("Erro ao buscar apostas");
      setApostas([]);
      setOrigem("");
    }
  };

  const fetchHistorico = async () => {
    try {
      const response = await fetch(`${API_URL}/historico-apostas`);
      const data = await response.json();
      setHistorico(data.historico || []);
    } catch (error) {
      setErro("Erro ao buscar histórico");
    }
  };

  const analisarAposta = async () => {
    try {
      setErro(null);
      const dezenas = inputDezenas
        .split(",")
        .map((d) => parseInt(d.trim()))
        .filter((n) => !isNaN(n));

      const response = await fetch(`${API_URL}/analisar-aposta`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ dezenas }),
      });

      const data = await response.json();

      if (data && data.score !== undefined) {
        setAnalise(data);
        setOrigem(data.origem);
      } else {
        setErro("Resposta inesperada da IA");
        setAnalise(null);
      }
    } catch (error) {
      setErro("Erro ao analisar a aposta");
      setAnalise(null);
    }
  };

  const contarRepeticoes = () => {
    const contagem = {};
    historico.forEach((item) => {
      item.dezenas.forEach((dezena) => {
        contagem[dezena] = (contagem[dezena] || 0) + 1;
      });
    });
    const pares = Object.entries(contagem)
      .sort((a, b) => b[1] - a[1])
      .map(([dez, qtd]) => `${dez}: ${qtd}x`);
    return pares;
  };

  const historicoFiltrado = historico.filter((item) =>
    filtro ? item.origem.includes(filtro) : true
  );

  return (
    <div className="App">
      <h2>🥳 Painel IA da Lotofácil 🤖</h2>

      <div>
        <button onClick={() => fetchApostas("gerar-apostas")}>Gerar Apostas</button>
        <button onClick={() => fetchApostas("gerar-aposta-bonus")}>Aposta Bônus</button>
        <button onClick={() => fetchApostas("gerar-aposta-experimental")}>Experimental</button>
        <button onClick={() => fetchApostas("gerar-aposta-refinada")}>Refinar</button>
        <button onClick={fetchHistorico}>📜 Ver Histórico</button>
      </div>

      <h3>📊 Apostas Geradas:</h3>
      {erro && <p style={{ color: "red" }}>❌ {erro}</p>}
      {origem && <p><strong>🧠 Função executada:</strong> {origem}</p>}
      <ul>
        {apostas.map((aposta, index) => (
          <li key={index}>{aposta.join(", ")}</li>
        ))}
      </ul>

      <h3>🧠 Analisar Aposta Manual:</h3>
      <input
        type="text"
        value={inputDezenas}
        onChange={(e) => setInputDezenas(e.target.value)}
        placeholder="Ex: 1,3,5,8,10,12,14,17..."
      />
      <button onClick={analisarAposta}>Analisar Aposta</button>

      {analise && (
        <div>
          <p>✅ <strong>Dezenas:</strong> {analise.dezenas.join(", ")}</p>
          <p>🔢 <strong>Pares:</strong> {analise.pares}</p>
          <p>🔢 <strong>Primos:</strong> {analise.primos}</p>
          <p>📘 <strong>Repetidas:</strong> {analise.repetidas}</p>
          <p>📊 <strong>Avaliação:</strong> {analise.avaliacao} (Score: {analise.score})</p>
        </div>
      )}

      <h3>📜 Histórico de Apostas:</h3>
      <input
        type="text"
        placeholder="Filtrar por tipo..."
        value={filtro}
        onChange={(e) => setFiltro(e.target.value)}
      />
      <ul>
        {historicoFiltrado.map((item, idx) => (
          <li key={idx}>
            <strong>{item.origem}</strong> | {item.data} → {item.dezenas.join(", ")}
          </li>
        ))}
      </ul>

      <h3>📈 Frequência de Dezenas (Todas):</h3>
      <ul>
        {contarRepeticoes().map((linha, idx) => (
          <li key={idx}>{linha}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
