const game=document.getElementById("game");
const player=document.getElementById("player");
const startBtn=document.getElementById("startBtn");
const restartBtn=document.getElementById("restartBtn");
const menu=document.getElementById("menu");
const pauseMenu=document.getElementById("pause");
const gameOver=document.getElementById("gameOver");
const crosshair=document.getElementById("crosshair");

const healthText=document.getElementById("health");
const scoreText=document.getElementById("score");
const waveText=document.getElementById("wave");
const coinText=document.getElementById("coins");
const staminaText=document.getElementById("stamina");
const waveBanner=document.getElementById("waveText");
const finalScore=document.getElementById("finalScore");

let playerX=window.innerWidth/2;
let playerY=window.innerHeight/2;
let playerSize=40;

let health=5;
let score=0;
let wave=1;
let coins=0;
let stamina=100;

let running=false;
let paused=false;

let speed=4;
let sprintSpeed=7;
let dashReady=true;

const keys={};

const zombies=[];
const bullets=[];
const particles=[];
const pickups=[];

const timerCard=document.createElement("div");
timerCard.className="card";
timerCard.innerHTML="⏱ <span id='time'>0</span>";
document.getElementById("hud").appendChild(timerCard);

let surviveTime=0;

setInterval(()=>{
if(running&&!paused){
surviveTime++;
document.getElementById("time").textContent=surviveTime;
}
},1000);

function updateHUD(){
healthText.textContent=health;
scoreText.textContent=score;
waveText.textContent=wave;
coinText.textContent=coins;
staminaText.textContent=Math.floor(stamina);
}

function updatePlayer(){
player.style.left=playerX+"px";
player.style.top=playerY+"px";
}

function showWave(text){
waveBanner.textContent=text;
waveBanner.style.opacity=1;
setTimeout(()=>{
waveBanner.style.opacity=0;
},1800);
}

document.addEventListener("mousemove",e=>{
crosshair.style.left=e.clientX+"px";
crosshair.style.top=e.clientY+"px";
});

document.addEventListener("keydown",e=>{

keys[e.key.toLowerCase()]=true;

if(e.key.toLowerCase()==="p"&&running){
paused=!paused;
pauseMenu.classList.toggle("hidden",!paused);
}

if(e.code==="Space"&&dashReady&&running&&!paused){

dashReady=false;

let dx=0;
let dy=0;

if(keys["w"]||keys["arrowup"])dy--;
if(keys["s"]||keys["arrowdown"])dy++;
if(keys["a"]||keys["arrowleft"])dx--;
if(keys["d"]||keys["arrowright"])dx++;

if(dx!==0||dy!==0){

const len=Math.hypot(dx,dy);

playerX+=dx/len*160;
playerY+=dy/len*160;

}

setTimeout(()=>{
dashReady=true;
},3000);

}

});

document.addEventListener("keyup",e=>{
keys[e.key.toLowerCase()]=false;
});

function movePlayer(){

if(!running||paused)return;

let currentSpeed=speed;

if(keys["shift"]&&stamina>0){

currentSpeed=sprintSpeed;
stamina-=0.8;

}else{

stamina+=0.4;

}

if(stamina<0)stamina=0;
if(stamina>100)stamina=100;

if(keys["w"]||keys["arrowup"])playerY-=currentSpeed;
if(keys["s"]||keys["arrowdown"])playerY+=currentSpeed;
if(keys["a"]||keys["arrowleft"])playerX-=currentSpeed;
if(keys["d"]||keys["arrowright"])playerX+=currentSpeed;

if(playerX<playerSize/2)playerX=playerSize/2;
if(playerY<playerSize/2)playerY=playerSize/2;

if(playerX>window.innerWidth-playerSize/2){
playerX=window.innerWidth-playerSize/2;
}

if(playerY>window.innerHeight-playerSize/2){
playerY=window.innerHeight-playerSize/2;
}

updatePlayer();
updateHUD();

}

startBtn.onclick=()=>{

menu.classList.add("hidden");

running=true;

showWave("Wave 1");

};

restartBtn.onclick=()=>{

location.reload();

};

window.addEventListener("resize",()=>{

if(playerX>window.innerWidth-playerSize/2){
playerX=window.innerWidth-playerSize/2;
}

if(playerY>window.innerHeight-playerSize/2){
playerY=window.innerHeight-playerSize/2;
}

updatePlayer();

});

updateHUD();
updatePlayer();
function createBullet(mx,my){

const bullet=document.createElement("div");
bullet.className="bullet";

const angle=Math.atan2(my-playerY,mx-playerX);

const speed=12;

const obj={
el:bullet,
x:playerX,
y:playerY,
vx:Math.cos(angle)*speed,
vy:Math.sin(angle)*speed,
life:90
};

bullet.style.left=obj.x+"px";
bullet.style.top=obj.y+"px";

game.appendChild(bullet);
bullets.push(obj);

}

document.addEventListener("mousedown",e=>{

if(!running||paused)return;

createBullet(e.clientX,e.clientY);

});

function updateBullets(){

for(let i=bullets.length-1;i>=0;i--){

const b=bullets[i];

b.x+=b.vx;
b.y+=b.vy;
b.life--;

b.el.style.left=b.x+"px";
b.el.style.top=b.y+"px";

if(
b.life<=0||
b.x<-30||
b.y<-30||
b.x>window.innerWidth+30||
b.y>window.innerHeight+30
){

b.el.remove();
bullets.splice(i,1);

}

}

}

function createParticles(x,y,color,count){

for(let i=0;i<count;i++){

const p=document.createElement("div");

p.className="particle";
p.style.background=color;

const obj={
el:p,
x:x,
y:y,
vx:(Math.random()-.5)*8,
vy:(Math.random()-.5)*8,
life:25+Math.random()*20
};

p.style.left=x+"px";
p.style.top=y+"px";

game.appendChild(p);
particles.push(obj);

}

}

function updateParticles(){

for(let i=particles.length-1;i>=0;i--){

const p=particles[i];

p.x+=p.vx;
p.y+=p.vy;

p.vx*=.96;
p.vy*=.96;

p.life--;

p.el.style.left=p.x+"px";
p.el.style.top=p.y+"px";
p.el.style.opacity=p.life/45;

if(p.life<=0){

p.el.remove();
particles.splice(i,1);

}

}

}

function spawnCoin(x,y){

const coin=document.createElement("div");
coin.className="coin";

coin.style.left=x+"px";
coin.style.top=y+"px";

game.appendChild(coin);

pickups.push({
type:"coin",
el:coin,
x:x,
y:y
});

}

function spawnHealth(){

const h=document.createElement("div");

h.style.position="absolute";
h.style.width="22px";
h.style.height="22px";
h.style.borderRadius="50%";
h.style.background="#22c55e";
h.style.boxShadow="0 0 12px #22c55e";

const x=Math.random()*(window.innerWidth-50);
const y=Math.random()*(window.innerHeight-50);

h.style.left=x+"px";
h.style.top=y+"px";

game.appendChild(h);

pickups.push({
type:"health",
el:h,
x:x,
y:y,
life:900
});

}

setInterval(()=>{

if(running&&!paused&&Math.random()<0.45){

spawnHealth();

}

},18000);

function updatePickups(){

for(let i=pickups.length-1;i>=0;i--){

const p=pickups[i];

if(p.life!==undefined){

p.life--;

if(p.life<=0){

p.el.remove();
pickups.splice(i,1);
continue;

}

}

const d=Math.hypot(playerX-p.x,playerY-p.y);

if(d<30){

if(p.type==="coin"){

coins+=1;

}

if(p.type==="health"){

if(health<5){

health++;

}

}

updateHUD();

createParticles(p.x,p.y,"gold",8);

p.el.remove();
pickups.splice(i,1);

}

}

}
function spawnZombie(type="normal"){

const zombie=document.createElement("div");
zombie.className="zombie";

let size=40;
let speed=1.4;
let hp=1;
let reward=10;

if(type==="fast"){
zombie.classList.add("fast");
speed=2.6;
hp=1;
reward=15;
}

if(type==="tank"){
zombie.classList.add("tank");
size=60;
speed=.8;
hp=4;
reward=30;
}

if(type==="boss"){
zombie.classList.add("tank");
size=120;
speed=.55;
hp=25;
reward=200;
zombie.style.background="#5b0f0f";
zombie.style.boxShadow="0 0 25px #ff0000";
}

let x;
let y;

if(Math.random()<.5){

x=Math.random()*window.innerWidth;
y=Math.random()<.5?-100:window.innerHeight+100;

}else{

x=Math.random()<.5?-100:window.innerWidth+100;
y=Math.random()*window.innerHeight;

}

zombie.style.width=size+"px";
zombie.style.height=size+"px";
zombie.style.left=x+"px";
zombie.style.top=y+"px";

game.appendChild(zombie);

zombies.push({
el:zombie,
x,
y,
size,
speed,
hp,
reward,
lastHit:0
});

}

function randomZombie(){

const r=Math.random();

if(r<.7)return"normal";
if(r<.9)return"fast";
return"tank";

}

function updateZombies(){

for(let i=zombies.length-1;i>=0;i--){

const z=zombies[i];

const angle=Math.atan2(playerY-z.y,playerX-z.x);

z.x+=Math.cos(angle)*z.speed;
z.y+=Math.sin(angle)*z.speed;

z.el.style.left=z.x+"px";
z.el.style.top=z.y+"px";

const hitDistance=(playerSize+z.size)/2;

if(Math.hypot(playerX-z.x,playerY-z.y)<hitDistance){

if(Date.now()-z.lastHit>700){

z.lastHit=Date.now();

health--;

updateHUD();

player.classList.add("damage");

document.body.animate(
[
{transform:"translate(6px,2px)"},
{transform:"translate(-6px,-2px)"},
{transform:"translate(4px,4px)"},
{transform:"translate(0,0)"}
],
{
duration:180
}
);

setTimeout(()=>{
player.classList.remove("damage");
},200);

if(health<=0){

running=false;

finalScore.textContent=score;

gameOver.classList.remove("hidden");

}

}

}

}

}

function checkBulletHits(){

for(let i=bullets.length-1;i>=0;i--){

const b=bullets[i];

for(let j=zombies.length-1;j>=0;j--){

const z=zombies[j];

const d=Math.hypot(b.x-z.x,b.y-z.y);

if(d<(z.size/2)+5){

createParticles(z.x,z.y,"#ef4444",12);

z.hp--;

b.el.remove();
bullets.splice(i,1);

if(z.hp<=0){

score+=z.reward;

if(Math.random()<.6){
spawnCoin(z.x,z.y);
}

z.el.remove();
zombies.splice(j,1);

updateHUD();

}

break;

}

}

}

}

setInterval(()=>{

if(running&&!paused){

spawnZombie(randomZombie());

}

},1400);
let waveKills=0;
let spawnDelay=1400;
let bossAlive=false;

function nextWave(){

wave++;
waveKills=0;

showWave("Wave "+wave);

updateHUD();

if(spawnDelay>450){
spawnDelay-=80;
}

clearInterval(spawnLoop);

spawnLoop=setInterval(()=>{

if(running&&!paused){

spawnZombie(randomZombie());

}

},spawnDelay);

if(wave%5===0&&!bossAlive){

bossAlive=true;

spawnZombie("boss");

}

}

const oldCheckBulletHits=checkBulletHits;

checkBulletHits=function(){

for(let i=bullets.length-1;i>=0;i--){

const b=bullets[i];

for(let j=zombies.length-1;j>=0;j--){

const z=zombies[j];

const d=Math.hypot(b.x-z.x,b.y-z.y);

if(d<(z.size/2)+5){

createParticles(z.x,z.y,"#ef4444",12);

z.hp--;

b.el.remove();
bullets.splice(i,1);

if(z.hp<=0){

score+=z.reward;
waveKills++;

if(Math.random()<0.6){
spawnCoin(z.x,z.y);
}

if(z.size>=120){
bossAlive=false;
}

z.el.remove();
zombies.splice(j,1);

updateHUD();

if(waveKills>=15+wave*2){

nextWave();

}

}

break;

}

}

}

};

let spawnLoop=setInterval(()=>{

if(running&&!paused){

spawnZombie(randomZombie());

}

},spawnDelay);

function gameLoop(){

requestAnimationFrame(gameLoop);

if(!running||paused)return;

movePlayer();
updateBullets();
updateParticles();
updatePickups();
updateZombies();
checkBulletHits();

}

gameLoop();

showWave("Zombie Escape");
updateHUD();
updatePlayer();