import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'https://lotofacil-api.onrender.com';

export default function App() {
  const [historico, setHistorico] = useState([]);
  const [frequencia, setFrequencia] = useState([]);
  const [filtroTipo, setFiltroTipo] = useState('');
  const [filtroData, setFiltroData] = useState('');
  const [erro, setErro] = useState('');

  const fetchHistorico = async () => {
    try {
      const response = await axios.get(`${API_URL}/historico`);
      setHistorico(response.data);
    } catch (err) {
      setErro('Erro ao carregar o histórico');
    }
  };

  const fetchFrequencia = async () => {
    try {
      const response = await axios.get(`${API_URL}/frequencia`);
      setFrequencia(response.data);
    } catch (err) {
      setErro('Erro ao carregar a frequência');
    }
  };

  useEffect(() => {
    fetchHistorico();
    fetchFrequencia();
  }, []);

  const historicoFiltrado = historico.filter((item) => {
    const matchTipo = filtroTipo ? item.origem === filtroTipo : true;
    const matchData = filtroData ? item.data.startsWith(filtroData) : true;
    return matchTipo && matchData;
  });

  return (
    <div style={{ padding: '20px' }}>
      <h2>Painel de Histórico de Apostas</h2>

      <div style={{ marginBottom: '20px' }}>
        <label>Filtrar por tipo: </label>
        <select onChange={(e) => setFiltroTipo(e.target.value)} value={filtroTipo}>
          <option value=''>Todos</option>
          <option value='gerar-apostas'>Gerar Apostas</option>
          <option value='aposta-bonus'>Aposta Bônus</option>
          <option value='aposta-experimental'>Aposta Experimental</option>
          <option value='refinar'>Refinar</option>
          <option value='analisar-aposta'>Análise Manual</option>
        </select>
        <input
          type='date'
          onChange={(e) => setFiltroData(e.target.value)}
          value={filtroData}
          style={{ marginLeft: '20px' }}
        />
      </div>

      {erro && <p style={{ color: 'red' }}>{erro}</p>}

      <h3>⭐ Dezenas Mais Repetidas</h3>
      <ul>
        {frequencia.map((item, idx) => (
          <li key={idx}>
            Dezena <strong>{item.dezena}</strong>: {item.quantidade}x
          </li>
        ))}
      </ul>

      <h3>🕛 Histórico de Apostas</h3>
      <ul>
        {historicoFiltrado.map((item, idx) => (
          <li key={idx} style={{ marginBottom: '10px' }}>
            <strong>{item.origem}</strong> - {item.data} <br />
            Dezenas: {item.dezenas.join(', ')}
          </li>
        ))}
      </ul>
    </div>
  );
}
