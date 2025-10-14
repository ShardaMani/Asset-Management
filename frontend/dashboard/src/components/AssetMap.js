import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './AssetMap.css';

// fix default icon paths for leaflet in CRA
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const fallbackBuildingCoords = {
  1: [12.989323212442327, 80.22908216128269],
  2: [28.6145, 77.2031],
  3: [28.6150, 77.2040],
  4: [28.6155, 77.2050],
  5: [28.6160, 77.2060],
};
// default center for the map (moved above useEffect so it's available when used)
const defaultCenter = [28.6152, 77.2045];

// helper: get building id from an asset (handles asset.building or asset.room.building)
const getBuildingId = (asset) => {
  if (!asset) return null;
  if (asset.building && asset.building.id) return Number(asset.building.id);
  if (asset.room && asset.room.building && asset.room.building.id) return Number(asset.room.building.id);
  return null;
};

export default function AssetMap() {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // debug toggles
  const DEBUG_SHOW_RAW = true;
  // show only one selected asset for POC (change as needed)
  const SELECT_ASSET_ID = 33;

  useEffect(() => {
    const API_BASE = (process.env.REACT_APP_API_URL || '').replace(/\/$/, '');
    const url = API_BASE ? `${API_BASE}/api/instances/map/` : '/api/instances/map/';
    console.log('[AssetMap] fetching', url, '(API_BASE=' + (API_BASE || '<empty>') + ')');
    fetch(url)
      .then(async (r) => {
        const ct = r.headers.get('content-type') || '';
        const text = await r.text();
        if (!r.ok) {
          console.error('[AssetMap] fetch not ok:', r.status, text);
          throw new Error(`HTTP ${r.status}`);
        }
        if (!ct.includes('application/json')) {
          console.warn('[AssetMap] expected JSON but got:', ct, text.slice(0, 200));
          try {
            return JSON.parse(text);
          } catch (e) {
            throw new Error('Response was not valid JSON');
          }
        }
        return JSON.parse(text);
      })
      .then((data) => {
        console.log('[AssetMap] data length', Array.isArray(data) ? data.length : 'not-array', data && data[0]);
  const arr = data || [];
  let newCenter = defaultCenter;
        // find the selected asset and its room id
        const sel = arr.find((x) => x && Number(x.id) === Number(SELECT_ASSET_ID));
        const selRoomId = sel && sel.room && sel.room.id ? Number(sel.room.id) : null;
    const selRoomCode = sel && sel.room && sel.room.room_code ? String(sel.room.room_code).trim() : null;
    // building id derived robustly (asset may have building nested in different places)
    const selBuildingId = getBuildingId(sel);
        // keep assets that either have explicit coords OR are in the same room as selected asset
        const filtered = arr.filter((a) => {
          if (!a) return false;
          if (a.latitude && a.longitude) return true;
           // match by room id
           if (selRoomId && a.room && a.room.id && Number(a.room.id) === selRoomId) return true;
           // match by room code (some rows may not have consistent ids)
           if (selRoomCode && a.room && a.room.room_code && String(a.room.room_code).trim() === selRoomCode) return true;
           // match by building id
           if (selBuildingId && a.room && a.room.building && a.room.building.id && Number(a.room.building.id) === selBuildingId) return true;
          return false;
        });
        setAssets(filtered);
        // compute center: prioritize selected asset coords or its building fallback
        if (sel) {
          if (sel.latitude && sel.longitude) {
            newCenter = [Number(sel.latitude), Number(sel.longitude)];
          } else if (selBuildingId && fallbackBuildingCoords[selBuildingId]) {
            newCenter = fallbackBuildingCoords[selBuildingId];
          } else if (filtered.length > 0) {
            // center on first filtered asset
            const a = filtered[0];
            if (a.latitude && a.longitude) newCenter = [Number(a.latitude), Number(a.longitude)];
            else {
              const aB = getBuildingId(a);
              if (aB && fallbackBuildingCoords[aB]) newCenter = fallbackBuildingCoords[aB];
            }
          }
        } else if (filtered.length > 0) {
          const a = filtered[0];
          if (a.latitude && a.longitude) newCenter = [Number(a.latitude), Number(a.longitude)];
          else {
            const aB = getBuildingId(a);
            if (aB && fallbackBuildingCoords[aB]) newCenter = fallbackBuildingCoords[aB];
          }
        } else {
          // fallback: keep defaultCenter
        }
        setCenter(newCenter);
      })
      .catch((err) => {
        console.error('map fetch error', err);
        setError(err.message || 'Fetch error');
      })
      .finally(() => setLoading(false));
  }, []);
  const [center, setCenter] = useState(defaultCenter);

  const getCoordsForAsset = (a) => {
    // prefer explicit lat/lon
    if (a.latitude && a.longitude) return [Number(a.latitude), Number(a.longitude)];
    // building-level fallback (room.building or asset.building)
    const b = a.building || (a.room && a.room.building);
    const base = (b && fallbackBuildingCoords[b.id]) ? fallbackBuildingCoords[b.id] : center;
    const idNum = Number(a.id) || Math.floor(Math.random() * 1000);

    // Compact square packing mode: tightly pack assets inside a small square around `base`.
    // This makes the cluster look congested and centered on the building coordinates.
    const MODE = 'COMPACT_SQUARE';
    if (MODE === 'COMPACT_SQUARE') {
      // half-side length of the square in degrees.
      // Smaller value => more congested. 0.00012 ~ ~13m (approx), good for a small building cluster.
      const halfSide = 0.00012;
      // determine grid size using the actual number of assets in the current filtered set
      const count = Math.max(assets && assets.length ? assets.length : 16, 1);
      const perSide = Math.ceil(Math.sqrt(count));
      // find a stable index for this asset inside the filtered assets list if possible
      const stableIndex = (() => {
        if (!assets || !Array.isArray(assets)) return idNum % (perSide * perSide);
        const idx = assets.findIndex(x => x && Number(x.id) === Number(a.id));
        return idx >= 0 ? idx : (idNum % (perSide * perSide));
      })();
      const row = Math.floor(stableIndex / perSide);
      const col = stableIndex % perSide;
      // normalize to [-0.5, 0.5]
      const nx = (perSide > 1) ? (col / (perSide - 1)) - 0.5 : 0;
      const ny = (perSide > 1) ? (row / (perSide - 1)) - 0.5 : 0;
      // cell spacing scaled to halfSide so entire grid fits within [-halfSide, +halfSide]
      const offsetLat = ny * (halfSide * 2);
      const offsetLng = nx * (halfSide * 2);
      return [base[0] + offsetLat, base[1] + offsetLng];
    }

    // fallback: circular distribution (shouldn't hit this when MODE is COMPACT_SQUARE)
    const radius = 0.0006; // ~60-70m max spread
    const goldenAngle = 2.399963229728653; // ~137.5deg
    const angle = (idNum * goldenAngle) % (2 * Math.PI);
    const ringFactor = ((idNum % 6) + 1) / 6;
    const r = ringFactor * radius;
    const offsetLat = Math.sin(angle) * r;
    const offsetLng = Math.cos(angle) * r;
    return [base[0] + offsetLat, base[1] + offsetLng];
  };

  if (loading) return <div style={{ padding: 12 }}>Loading map data…</div>;
  if (error) return <div style={{ padding: 12, color: 'crimson' }}>Error loading map data: {error}</div>;

  return (
    <div style={{ height: '85vh', width: '100%', position: 'relative' }}>
      {/* floating info panel */}
      {DEBUG_SHOW_RAW && (
        <div className="map-panel">
          <div className="map-panel-title">Map info</div>
          <div className="map-panel-row">Assets: <strong>{assets.length}</strong></div>
          <div className="map-panel-row">Center: <small>{center.join(', ')}</small></div>
          {/* only show counts and center now - names removed per UX request */}
        </div>
      )}

      {/* render MapContainer only after we have a center and force remount when center changes via key */}
      {center && (
        <MapContainer key={String(center)} id="leaflet-map" center={center} zoom={16} style={{ height: '100%', width: '100%', border: '2px dashed rgba(0,0,0,0.2)' }}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {assets.map((a) => {
          const coords = getCoordsForAsset(a);
          return (
            <Marker key={a.id} position={coords}>
              <Popup>
                <div style={{ minWidth: 220 }}>
                  <strong>{a.tag || a.label || `Asset ${a.id}`}</strong>
                  <div>Model: {a.asset_model?.model_name || '-'}</div>
                  <div>Building: {a.building?.name || '-'}</div>
                  <div>Room: {a.room?.room_code || '-'}</div>
                  <div>Status: {a.is_active ? 'Active' : 'Inactive'}</div>
                  <div style={{ marginTop: 6, fontSize: 12 }}>{a.description || ''}</div>
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
      )}
    </div>
  );
}