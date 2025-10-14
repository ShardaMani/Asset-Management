import React from 'react';
import './HeroBanner.css';

export default function HeroBanner({ assetsCount = 0, buildingsCount = 0, roomsCount = 0 }) {
  const scrollToMap = () => {
    const el = document.getElementById('leaflet-map');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <section className="hero-banner">
      <div className="hero-inner">
        <h2 className="hero-title">IIT Madras Campus Asset Management</h2>
        <p className="hero-sub">Advanced tracking and analytics for campus resources</p>
        <div className="hero-divider" />

        <div className="hero-stats">
          <div className="hero-stat">
            <div className="hero-number">{assetsCount}+ </div>
            <div className="hero-label">entities recorded</div>
          </div>
          <div className="hero-stat">
            <div className="hero-number">{buildingsCount} </div>
            <div className="hero-label">buildings located</div>
          </div>
          <div className="hero-stat">
            <div className="hero-number">{roomsCount} </div>
            <div className="hero-label">rooms mapped</div>
          </div>
        </div>

        <div style={{ marginTop: 18 }}>
          <button className="hero-cta" onClick={scrollToMap}>Explore Map</button>
        </div>
      </div>
    </section>
  );
}
