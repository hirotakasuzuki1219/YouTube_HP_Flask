// 地図の初期表示
var map = L.map('map').setView([35.68, 139.76], 5);

// 背景地図
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
}).addTo(map);

// 旅のデータ
var travels = [
  {
    name: "京都",
    lat: 35.01,
    lon: 135.77,
    note: "紅葉が綺麗だった！",
    youtube: "https://www.youtube.com/embed/動画ID"
  },
  {
    name: "東京",
    lat: 35.68,
    lon: 139.76,
    note: "出発地！",
    youtube: "https://www.youtube.com/embed/動画ID2"
  }
];

// ピンを追加
travels.forEach(t => {
  L.marker([t.lat, t.lon])
   .addTo(map)
   .bindPopup(
     `<b>${t.name}</b><br>${t.note}<br>
      <iframe width="200" height="113" src="${t.youtube}" frameborder="0" allowfullscreen></iframe>`
   );
});
