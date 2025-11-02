// 地図の初期表示
var map = L.map('map').setView([35.776366, 140.386249], 2);

// 背景地図
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
}).addTo(map);

// 旅のデータ
var travels = [
  {
    name: "成田国際空港",
    lat: 35.776366,
    lon: 140.386249,
    note: "ここから世界一周をスタート！まずはエジプトへ",
    youtube: "https://www.youtube.com/embed/MsZmu32UglE"
  },
  {
    name: "エジプト・ギザ周辺",
    lat: 29.972883, 
    lon: 31.128796,
    note: "ピラミッド周辺を観光ツアーに参加",
    youtube: "https://www.youtube.com/embed/_1sYoq9pQWg"
  },
    {
    name: "大エジプト博物館入場",
    lat: 29.995239, 
    lon: 31.119273,
    note: "プレオープン中のレアな時期に潜入",
    youtube: "https://www.youtube.com/embed/-6LvRT89h_k"
  },
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
