// App.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [apostas, setApostas] = useState([]);
  const [apostaBonus, setApostaBonus] = useState(null);
  const [apostaExperimental, setApostaExperimental] = useState(null);
  const [apostaRefinada, setApostaRefinada] = useState(null);
  const [historico, setHistorico] = useState([]);
  const [frequencia, setFrequencia] = useState([]);
  const [resposta, setResposta] = useState("");

  useEffect(() => {
    fetchHistorico();
    fetchFrequencia();
  }, []);

  const fetchApostas = async () => {
    try {
      const response = await axios.get("https://lotofacil-api.onrender.com/gerar-apostas");
      setApostas(response.data.apostas || []);
      setResposta("Apostas geradas com sucesso.");
    } catch (error) {
      console.error("Erro ao gerar apostas:", error);
      setResposta("Erro ao gerar aposta.");
    }
  };

  const fetchBonus = async () => {
    try {
      const response = await axios.get("https://lotofacil-api.onrender.com/gerar-aposta-bonus");
      setApostaBonus(response.data.aposta);
    } catch (error) {
      console.error("Erro ao gerar bônus:", error);
    }
  };

  const fetchExperimental = async () => {
    try {
      const response = await axios.get("https://lotofacil-api.onrender.com/gerar-aposta-experimental");
      setApostaExperimental(response.data.aposta);
    } catch (error) {
      console.error("Erro ao gerar experimental:", error);
    }
  };

  const fetchRefinada = async () => {
    try {
      const response = await axios.get("https://lotofacil-api.onrender.com/gerar-aposta-refinada");
      setApostaRefinada(response.data.aposta);
    } catch (error) {
      console.error("Erro ao gerar refinada:", error);
    }
  };

  const fetchHistorico = async () => {
    try {
      const response = await axios.get("https://lotofacil-api.onrender.com/historico");
      setHistorico(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error("Erro ao buscar histórico:", error);
    }
  };

  const fetchFrequencia = async () => {
    try {
      const response = await axios.get("https://lotofacil-api.onrender.com/frequencia");
      const dados = response.data;
      setFrequencia(Array.isArray(dados) ? dados : []);
    } catch (error) {
      console.error("Erro ao buscar frequência:", error);
      setFrequencia([]);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Painel IA da Lotofácil</h2>

      <button onClick={fetchApostas}>Gerar Aposta</button>
      <button onClick={fetchRefinada}>Refinar Aposta</button>
      <button onClick={fetchExperimental}>Status da IA</button>
      <button onClick={fetchBonus}>Enviar Resultado Real</button>

      {resposta && <p><strong>Resposta:</strong> {resposta}</p>}

      <hr />
      <h3>Histórico de Apostas</h3>
      {historico.length === 0 ? (
        <p>Nenhuma aposta encontrada.</p>
      ) : (
        <ul>
          {historico.map((item, index) => (
            <li key={index}>
              <strong>{item.tipo}</strong> | {item.data} | {item.dezenas.join(", ")}
            </li>
          ))}
        </ul>
      )}

      <h3>Dezenas Mais Repetidas</h3>
      {frequencia.length === 0 ? (
        <p>Frequência ainda não disponível.</p>
      ) : (
        <ul>
          {frequencia.map((item, index) => (
            <li key={index}>
              Dezena {item.dezena}: {item.frequencia}x
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
