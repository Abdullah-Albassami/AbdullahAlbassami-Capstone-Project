// Optional verification only: installed Chrome + Node, no frontend dependencies.
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {randomBytes} from 'node:crypto';
import {mkdtemp, mkdir, rm, writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {dirname, join, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createInterface} from 'node:readline';

const appDir = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const temporary = await mkdtemp(join(tmpdir(), 'helpdesk-browser-'));
const evidence = process.env.HELPDESK_BROWSER_EVIDENCE || await mkdtemp(join(tmpdir(), 'helpdesk-browser-evidence-'));
await mkdir(evidence, {recursive: true});
const password = randomBytes(32).toString('base64url');
const results = [];
let server, chrome, sessionId, currentWidth, nextId = 0, buffer = '';
const pending = new Map();
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
function command(method, params = {}, session = sessionId) {
  const id = ++nextId;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {pending.delete(id); reject(new Error(method + ' timed out'));}, 15000);
    pending.set(id, {resolve, reject, timer});
    chrome.stdio[3].write(JSON.stringify({id, method, params, ...(session ? {sessionId: session} : {})}) + '\0');
  });
}
async function evaluate(expression) {
  const result = await command('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true});
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
  return result.result.value;
}
async function waitFor(check, description) {
  for (let attempt = 0; attempt < 150; attempt++) {
    try {if (await check()) return;} catch { /* navigation may replace the execution context */ }
    await pause(50);
  }
  throw new Error('Browser did not reach: ' + description);
}
async function navigate(path) {
  const result = await command('Page.navigate', {url: origin + path});
  assert(!result.errorText, result.errorText);
  await waitFor(async () => (await command('Page.getFrameTree')).frameTree.frame.loaderId === result.loaderId &&
    await evaluate("document.readyState === 'complete' && !!document.querySelector('main')"), path);
}
async function submit(selector, values = {}) {
  const oldLoader = (await command('Page.getFrameTree')).frameTree.frame.loaderId;
  await evaluate(`(() => {const form=document.querySelector(${JSON.stringify(selector)}); if(!form) throw new Error('Missing form');
    for(const [name,value] of Object.entries(${JSON.stringify(values)})) form.elements.namedItem(name).value=value;
    form.requestSubmit();})()`);
  await waitFor(async () => (await command('Page.getFrameTree')).frameTree.frame.loaderId !== oldLoader &&
    await evaluate("document.readyState === 'complete' && !!document.querySelector('main')"), 'form submission');
}
async function textIncludes(text) {assert(await evaluate(`document.body.innerText.includes(${JSON.stringify(text)})`), text);}
async function login(username) {
  await navigate('/accounts/login/');
  await submit('main form', {username, password});
  assert.equal(await evaluate('location.pathname'), '/');
}
async function logout() {await submit('nav form'); assert.equal(await evaluate('location.pathname'), '/accounts/login/');}
async function viewport(width) {
  currentWidth = width;
  await command('Emulation.setDeviceMetricsOverride', {width, height: 900, deviceScaleFactor: 1, mobile: width < 600});
}
async function auditPage(label) {
  const audit = await evaluate(`(() => {
    const ids=[...document.querySelectorAll('[id]')].map(node=>node.id);
    const unlabeled=[...document.querySelectorAll('input:not([type=hidden]),select,textarea')].filter(node=>!node.labels?.length);
    const described=[...document.querySelectorAll('[aria-describedby]')].every(node=>node.getAttribute('aria-describedby').split(' ').every(id=>document.getElementById(id)));
    const rgb=color=>color.match(/[\\d.]+/g).slice(0,3).map(Number);
    const luminance=color=>rgb(color).map(n=>n/255).map(n=>n<=.04045?n/12.92:((n+.055)/1.055)**2.4).reduce((sum,n,index)=>sum+n*[.2126,.7152,.0722][index],0);
    const ratio=(a,b)=>{const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);};
    const background=node=>{while(node){const color=getComputedStyle(node).backgroundColor;if(color!=='rgba(0, 0, 0, 0)')return color;node=node.parentElement;}return 'rgb(255, 255, 255)';};
    const contrastFailures=[];
    for(const node of document.querySelectorAll('a,button,label,p,h1,h2,h3,th,td,span,strong,small,input:not([type=hidden]),select,textarea')) {
      const rect=node.getBoundingClientRect(),style=getComputedStyle(node);
      if(rect.width<2||rect.height<2||style.visibility==='hidden')continue;
      const large=parseFloat(style.fontSize)>=24||(parseFloat(style.fontSize)>=18.6667&&Number(style.fontWeight)>=700);
      if(ratio(style.color,background(node))<(large?3:4.5))contrastFailures.push(node.tagName+' text');
      if(node.matches('input,select,textarea')&&ratio(style.borderTopColor,background(node))<3)contrastFailures.push(node.tagName+' boundary');
    }
    return {width:innerWidth, scrollWidth:document.documentElement.scrollWidth, unique:ids.length===new Set(ids).size,
      labels:unlabeled.length===0, described, landmarks:!!document.querySelector('header')&&!!document.querySelector('main')&&!!document.querySelector('footer'),
      css:getComputedStyle(document.body).backgroundColor==='rgb(245, 247, 251)',contrastFailures};
  })()`);
  assert(audit.unique && audit.labels && audit.described && audit.landmarks && audit.css, label + ': markup/CSS');
  assert.deepEqual(audit.contrastFailures,[],label+': contrast');
  assert(audit.width === currentWidth && audit.scrollWidth <= currentWidth + 1, label + ': viewport overflow ' + JSON.stringify(audit));
  results.push({label, ...audit});
}
async function screenshot(name) {
  const image = await command('Page.captureScreenshot', {format: 'png', captureBeyondViewport: true});
  await writeFile(join(evidence, name + '.png'), Buffer.from(image.data, 'base64'));
}
async function key(key, code, modifiers = 0) {
  const windowsVirtualKeyCode = {Tab:9,Enter:13,ArrowDown:40,ArrowRight:39}[key] || 0;
  await command('Input.dispatchKeyEvent', {type:'keyDown', key, code, modifiers, windowsVirtualKeyCode});
  await command('Input.dispatchKeyEvent', {type:'keyUp', key, code, modifiers, windowsVirtualKeyCode});
}
let origin;
try {
  server = spawn(join(appDir, '.venv/bin/python'), ['-B', join(appDir, 'scripts/browser_fixture.py')], {cwd: appDir,
    env: {...process.env, DJANGO_SECRET_KEY: randomBytes(64).toString('base64url'), DJANGO_DEBUG:'false',
      DEMO_PASSWORD:password, HELPDESK_BROWSER_DB:join(temporary,'browser.sqlite3')}, stdio:['ignore','pipe','pipe']});
  let serverError = '';
  server.stderr.on('data', data => {serverError=(serverError+data).slice(-1500);});
  const port = await new Promise((resolve,reject)=>{
    const lines=createInterface({input:server.stdout});
    lines.once('line', line=>{lines.close(); resolve(Number(line));});
    server.once('exit',()=>reject(new Error('Fixture server stopped: '+serverError)));
  });
  assert(port > 0);
  origin='http://127.0.0.1:'+port;
  chrome=spawn(process.env.HELPDESK_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    ['--headless=new','--remote-debugging-pipe','--no-first-run','--no-default-browser-check','--disable-background-networking',
      '--user-data-dir='+join(temporary,'chrome')], {stdio:['ignore','ignore','ignore','pipe','pipe']});
  chrome.stdio[4].on('data',data=>{
    buffer+=data; let index;
    while((index=buffer.indexOf('\0')) >= 0) {
      const part=buffer.slice(0,index); buffer=buffer.slice(index+1); if(!part) continue;
      const message=JSON.parse(part), waiter=pending.get(message.id);
      if(waiter) {pending.delete(message.id); clearTimeout(waiter.timer); message.error ? waiter.reject(new Error(message.error.message)) : waiter.resolve(message.result);}
    }
  });
  const version=await command('Browser.getVersion',{},null);
  const target=await command('Target.createTarget',{url:'about:blank'},null);
  sessionId=(await command('Target.attachToTarget',{targetId:target.targetId,flatten:true},null)).sessionId;
  await command('Page.enable');
  await viewport(1280);
  await navigate('/accounts/login/');
  await auditPage('login desktop');
  // Actual Shift-Tab and Enter input: autofocus starts on username.
  await key('Tab','Tab',8); await key('Tab','Tab',8);
  assert.equal(await evaluate('document.activeElement.className'),'skip-link');
  assert(await evaluate("getComputedStyle(document.activeElement).outlineStyle==='solid' && document.activeElement.getBoundingClientRect().top >= 0"));
  await key('Enter','Enter');
  assert.equal(await evaluate('document.activeElement.id'),'main-content');
  results.push({label:'keyboard skip link and visible focus',pass:true});
  await viewport(375); await auditPage('login mobile'); await screenshot('login-mobile');
  await login('itadmin');
  const cards=await evaluate("[...document.querySelectorAll('.metric strong')].map(n=>Number(n.textContent))");
  assert.deepEqual(cards,[12,8,2,2]);
  for(const width of [1280,375]) {
    await viewport(width);
    for(const path of ['/','/tickets/','/tickets/new/','/tickets/10001/','/tickets/10001/edit/','/tickets/10001/cancel/',
      '/tickets/10007/','/tickets/10009/','/tickets/10011/','/categories/','/categories/new/','/categories/1201/','/categories/1201/edit/','/categories/1201/delete/']) {
      await navigate(path); await auditPage(path+' at '+width);
    }
  }
  await navigate('/'); await screenshot('dashboard-mobile');
  await viewport(1280); await screenshot('dashboard-desktop');
  await navigate('/tickets/10001/');
  await textIncludes('Assign ticket');
  assert(await evaluate("[...document.querySelector('#id_assigned_to').options].some(option=>option.textContent==='Lina Demo (technician1)'&&option.value==='9003')"));
  await evaluate("document.querySelector('#id_assigned_to').focus()");
  await key('ArrowDown','ArrowDown');
  assert.equal(await evaluate("document.querySelector('#id_assigned_to').value"),'9003');
  results.push({label:'keyboard native technician selection',pass:true});
  await submit('form[action$="/assign/"]',{assigned_to:'9003'});
  await textIncludes('Assigned');
  await logout(); await login('technician1');
  await navigate('/tickets/10001/');
  await submit('form[action$="/start/"]');
  await submit('form[action$="/comment/"]',{body:'Browser check: cable tested.'});
  await submit('form[action$="/resolve/"]',{resolution_note:'Browser check: cable replaced; printing verified.'});
  await textIncludes('read-only');
  assert.equal(await evaluate("document.querySelectorAll('main form').length"),0);
  await logout(); await login('employee1'); await navigate('/tickets/10001/');
  await textIncludes('Browser check: cable tested.'); await textIncludes('printing verified');
  assert.equal(await evaluate("document.querySelectorAll('main form').length"),0);
  await navigate('/categories/'); await textIncludes('Access restricted');
  await navigate('/tickets/10004/'); await textIncludes('Page unavailable');
  await navigate('/tickets/new/');
  await evaluate("document.querySelector('main form').noValidate=true");
  await submit('main form',{title:'   ',description:'   '});
  await textIncludes('Please correct'); await auditPage('bound ticket errors');
  await submit('main form',{title:'Browser acceptance request',description:'Fictional support issue for verification.',category:'1201',department:'1101',priority:'high'});
  const createdPath=await evaluate('location.pathname');
  await submit('form[action$="/comment/"]',{body:'Retain this discussion.'});
  await navigate(createdPath+'cancel/'); await submit('main form');
  await textIncludes('cancelled and read-only'); await textIncludes('Retain this discussion.');
  await logout(); await login('itadmin');
  assert.deepEqual(await evaluate("[...document.querySelectorAll('.metric strong')].map(n=>Number(n.textContent))"),[13,7,3,3]);
  await navigate('/categories/new/');
  await submit('main form',{name:'Browser category',description:'Temporary browser fixture'});
  const categoryPath=await evaluate('location.pathname');
  await navigate(categoryPath+'edit/'); await submit('main form',{name:'Browser category updated',description:'Updated fixture'});
  await navigate(categoryPath+'delete/'); await submit('main form'); await textIncludes('deleted');
  await navigate('/categories/1201/delete/'); await submit('main form'); await textIncludes('cannot be deleted');
  await viewport(375);
  await navigate('/tickets/?order=oldest&page=2'); await textIncludes('Page 2 of 2');
  await evaluate("document.querySelector('.table-wrapper').focus()");
  const beforeScroll=await evaluate("document.querySelector('.table-wrapper').scrollLeft");
  await key('ArrowRight','ArrowRight');
  await pause(250);
  assert(await evaluate("document.querySelector('.table-wrapper').scrollLeft")>beforeScroll);
  results.push({label:'keyboard horizontal ticket table scrolling',pass:true});
  await navigate('/tickets/?q=no_matching_issue'); await textIncludes('No matching tickets');
  await navigate('/tickets/?status=invalid&priority=high'); await textIncludes('Invalid filters were ignored');
  await navigate('/tickets/10001/start/'); await textIncludes('Use the page controls');
  await auditPage('friendly unsupported-method page');
  // Maximum model lengths must remain usable at a narrow viewport.
  await viewport(375);
  await navigate('/categories/new/');
  await submit('main form',{name:'C'.repeat(100),description:'Maximum-length category name'});
  const longCategory=await evaluate('location.pathname');
  await navigate(longCategory+'delete/');
  await screenshot('long-category-confirmation');
  await auditPage('maximum category name confirmation mobile');
  await navigate('/tickets/new/');
  await submit('main form',{title:'T'.repeat(150),description:'Maximum-length ticket title',category:'1201',department:'1101',priority:'low'});
  const longTicket=await evaluate('location.pathname');
  await navigate(longTicket+'cancel/');
  await screenshot('long-ticket-confirmation');
  await auditPage('maximum ticket title confirmation mobile');
  await logout(); await login('browser_setup');
  await navigate('/admin/tickets/ticket/10001/change/');
  assert.equal(await evaluate("document.querySelectorAll('input[name=_save],input[name=_continue],a.deletelink').length"),0);
  await navigate('/admin/tickets/ticketcomment/20001/change/');
  assert.equal(await evaluate("document.querySelectorAll('input[name=_save],input[name=_continue],a.deletelink').length"),0);
  await navigate('/admin/auth/user/9003/change/');
  await evaluate("document.querySelector('#id_is_active').checked=false");
  await submit('#user_form');
  await textIncludes("Reassign this account's active tickets");
  await submit('#logout-form');
  await login('technician1');
  results.push({label:'guarded admin read-only ticket/comment and active-technician safeguard',pass:true});
  results.push({label:'browser role lifecycle, terminal controls, authorization, validation, cancellation, Category CRUD/PROTECT and list edge states',pass:true});
  await writeFile(join(evidence,'results.json'),JSON.stringify({browser:version.product,results},null,2));
  console.log(JSON.stringify({browser:version.product,checks:results.length,result:'PASS',evidence}));
} finally {
  for(const child of [chrome,server]) if(child && child.exitCode===null && child.signalCode===null) {
    const exited=new Promise(resolve=>child.once('exit',resolve)); child.kill(); await exited;
  }
  for(const waiter of pending.values()) clearTimeout(waiter.timer);
  await rm(temporary,{recursive:true,force:true});
}
