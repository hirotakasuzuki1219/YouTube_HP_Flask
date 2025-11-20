// 地図の初期表示
var map = L.map('map').setView([35.776366, 140.386249], 1);

// 背景地図
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
}).addTo(map);

// 旅行データをデータベースから取得
var travels = [];

// APIからデータを取得
fetch('/api/travels')
  .then(response => response.json())
  .then(data => {
    travels = data;
    // ピンを追加
    travels.forEach(t => {
      L.marker([t.lat, t.lon])
        .addTo(map)
        .bindPopup(
          `<b>${t.name}</b><br>${t.note || ''}<br>
          ${t.youtube ? `<iframe width="200" height="113" src="${t.youtube}" frameborder="0" allowfullscreen></iframe>` : ''}`
        );
    });
    
    // データがある場合、最初の地点に地図をズーム
    if (travels.length > 0) {
      const bounds = L.latLngBounds(travels.map(t => [t.lat, t.lon]));
      map.fitBounds(bounds);
    }
  })
  .catch(error => {
    console.error('データの取得に失敗しました:', error);
    // エラー時は地図だけを表示
  });
