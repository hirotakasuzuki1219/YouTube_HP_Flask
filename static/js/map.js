// 地図の初期表示
var map = L.map('map').setView([35.776366, 140.386249], 1);

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
    name: "大エジプト博物館",
    lat: 29.995239, 
    lon: 31.119273,
    note: "プレオープン中のレアな時期に潜入",
    youtube: "https://www.youtube.com/embed/-6LvRT89h_k"
  },
  {
    name: "カイロ観光",
    lat: 30.046261, 
    lon: 31.262404,
    note: "アズハルモスクなどカイロ観光を堪能",
    youtube: "https://www.youtube.com/embed/F1OhTilyzu0"
  },
  {
    name: "カイロ脱出",
    lat: 30.015892, 
    lon: 31.224700,
    note: "閉じ込められて詰んだ",
    youtube: "https://www.youtube.com/embed/k6KMBY0qDo8"
  },
  {
    name: "カイロ国際空港",
    lat: 30.12177042996925, 
    lon: 31.416275346081747, 
    note: "トルコへ移動！",
    youtube: "https://www.youtube.com/embed/X7AN2xgwFTk"
  },
  {
    name: "イスタンブール",
    lat: 41.00539177063419, 
    lon: 28.96329556546734, 
    note: "イスタンブールでの日常を堪能",
    youtube: "https://www.youtube.com/embed/_ubQxQfXTrw"
  },
  {
    name: "アヤソフィアなど",
    lat: 41.009284623958024,  
    lon: 28.980010132269836, 
    note: "イスタンブール観光！",
    youtube: "https://www.youtube.com/embed/T-THt_l9TKQ"
  },
  {
    name: "ザビハ・ギョクチェン国際空港",
    lat: 40.89569332688844, 
    lon: 29.313471511623103, 
    note: "次の目的地カッパドキアへ！",
    youtube: "https://www.youtube.com/embed/fmsuShXs0Ds"
  },
  {
    name: "カッパドキア",
    lat: 38.63997623195001, 
    lon: 34.832035222971506, 
    note: "カッパドキアといえば熱気球！",
    youtube: "https://www.youtube.com/embed/M-5Dgpj45xo"
  },
  {
    name: "ローズバレー",
    lat: 38.659307136759445, 
    lon: 34.843411955828536, 
    note: "無料の大冒険！",
    youtube: "https://www.youtube.com/embed/MiYJTreMAgY"
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
