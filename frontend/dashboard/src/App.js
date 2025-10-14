import './App.css';
import React, { useEffect, useState } from 'react';
import AssetMap from './components/AssetMap';
import HeroBanner from './components/HeroBanner';

function App() {
  const [assetsCount, setAssetsCount] = useState(0);
  const [buildingsCount, setBuildingsCount] = useState(0);
  const [roomsCount, setRoomsCount] = useState(0);

  useEffect(() => {
    // fetch asset list to compute simple counts for the hero banner
    const API_BASE = (process.env.REACT_APP_API_URL || '').replace(/\/$/, '');
    const url = API_BASE ? `${API_BASE}/api/instances/map/` : '/api/instances/map/';
    fetch(url)
      .then((r) => r.json())
      .then((data) => {
        const arr = Array.isArray(data) ? data : [];
        setAssetsCount(arr.length);
        const bSet = new Set();
        const rSet = new Set();
        arr.forEach((a) => {
          if (a && a.room && a.room.building && a.room.building.id) bSet.add(a.room.building.id);
          if (a && a.room && a.room.id) rSet.add(a.room.id);
        });
        setBuildingsCount(bSet.size);
        setRoomsCount(rSet.size);
      })
      .catch(() => {
        // leave zeros if error
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1 style={{ margin: 0, fontSize: 18 }}>IIT Madras Asset Management</h1>
      </header>

      <main className="App-main">
        <HeroBanner assetsCount={assetsCount} buildingsCount={buildingsCount} roomsCount={roomsCount} />
        <AssetMap />
      </main>
    </div>
  );
}

export default App;