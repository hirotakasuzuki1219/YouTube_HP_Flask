// 地図の初期表示
var map = L.map('map').setView([35.68, 139.76], 5);

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
    youtube: "https://www.youtube.com/embed/vH0D62mrzXM"
  },
  {
    name: "エジプト・ギザ周辺",
    lat: 29.972883, 
    lon: 31.128796,
    note: "ピラミッド周辺を観光ツアーに参加",
    youtube: "https://www.youtube.com/embed/_1sYoq9pQWg"
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
