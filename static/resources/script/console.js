(function() {
var STATIC_POWER = 10;
var MAX_LINES = 10;
var CHART_INTERVAL = 2000;
var CHART_POINTS = 30;

var outputEl = document.getElementById('console-output');
var inputEl = document.getElementById('console-input');
var chartEl = document.getElementById('console-chart');
if (!outputEl || !inputEl || !chartEl) return;

var lines = [];
var currentPower = 0;
var activeCommand = null;

var powerHistory = [];
for (var i = 0; i < CHART_POINTS; i++) {
  powerHistory.push(STATIC_POWER + (Math.random() - 0.5));
}

function render() {
  var display = lines.slice(-MAX_LINES);
  while (display.length < MAX_LINES) display.unshift('');
  outputEl.innerHTML = display.map(function(l) {
    return '<div class="console-line">' + escapeHtml(l) + '&nbsp;</div>';
  }).join('');
}

function escapeHtml(s) {
  var d = document.createElement('div');
  d.appendChild(document.createTextNode(s));
  return d.innerHTML;
}

function pushLine(text) {
  lines.push(text);
}

var commands = [];
if (typeof CONSOLE_COMMANDS !== 'undefined') {
  if (typeof CONSOLE_COMMANDS === 'string') {
    try { commands = JSON.parse(CONSOLE_COMMANDS); } catch(e) {}
  } else if (Array.isArray(CONSOLE_COMMANDS)) {
    commands = CONSOLE_COMMANDS;
  }
}

function findCommand(name) {
  for (var i = 0; i < commands.length; i++) {
    if (commands[i].name === name) return commands[i];
  }
  return null;
}

function handleInput(raw) {
  pushLine('$ ' + raw);
  var parts = raw.trim().split(/\s+/);
  var cmd = parts[0];
  var arg = parts.length > 1 ? parts.slice(1).join(' ') : null;

  if (!cmd) { render(); return; }

  if (cmd === 'help' || cmd === '?') {
    pushLine('Available commands:');
    pushLine('  help    - Show this help message');
    pushLine('  clear   - Clear the terminal');
    pushLine('  kill    - Kill running process (reset power to 0)');
    for (var i = 0; i < commands.length; i++) {
      var c = commands[i];
      pushLine('  ' + c.name + '    - ' + c.help);
    }
    render();
    return;
  }

  if (cmd === 'clear') {
    lines = [];
    render();
    return;
  }

  if (cmd === 'kill') {
    currentPower = 0;
    activeCommand = null;
    pushLine('process killed');
    render();
    return;
  }

  var def = findCommand(cmd);
  if (!def) {
    pushLine(cmd + ': command not found. Type help or ? for available commands.');
    render();
    return;
  }

  if (def.params && def.params.length > 0) {
    var matched = null;
    if (arg === null) {
      for (var j = 0; j < def.params.length; j++) {
        if (def.params[j]['default']) { matched = def.params[j]; break; }
      }
      if (!matched) {
        pushLine(cmd + ': missing parameter');
        render();
        return;
      }
    } else {
      for (var j = 0; j < def.params.length; j++) {
        if (String(def.params[j].value) === arg) { matched = def.params[j]; break; }
      }
    }
    if (!matched) {
      pushLine(cmd + ': invalid parameter "' + arg + '"');
      render();
      return;
    }
    if (activeCommand === cmd && def.replace_message) {
      pushLine(def.replace_message);
    }
    pushLine(matched.output);
    currentPower = matched.power || 0;
    activeCommand = cmd;
  } else {
    pushLine(def.output);
  }

  render();
}

var builtins = ['help', 'clear', 'kill'];
var tabMatches = [];
var tabIndex = -1;
var tabPrefix = '';
var history = [];
var historyIndex = -1;

function getCompletions(text) {
  var parts = text.split(/\s+/);
  if (parts.length <= 1) {
    var prefix = parts[0] || '';
    var all = builtins.slice();
    for (var i = 0; i < commands.length; i++) all.push(commands[i].name);
    return all.filter(function(n) { return n.indexOf(prefix) === 0; });
  }
  var cmd = parts[0];
  var def = findCommand(cmd);
  if (def && def.params) {
    var argPrefix = parts[parts.length - 1] || '';
    return def.params
      .map(function(p) { return String(p.value); })
      .filter(function(v) { return v.indexOf(argPrefix) === 0; })
      .map(function(v) { return cmd + ' ' + v; });
  }
  return [];
}

inputEl.addEventListener('keydown', function(e) {
  if (e.key === 'Tab') {
    e.preventDefault();
    var current = inputEl.value;
    if (tabMatches.length === 0 || current !== tabMatches[tabIndex]) {
      tabPrefix = current;
      tabMatches = getCompletions(tabPrefix);
      tabIndex = -1;
    }
    if (tabMatches.length > 0) {
      tabIndex = (tabIndex + 1) % tabMatches.length;
      inputEl.value = tabMatches[tabIndex];
    }
    return;
  }
  tabMatches = [];
  tabIndex = -1;
  if (e.key === 'ArrowUp') {
    e.preventDefault();
    if (history.length > 0 && historyIndex < history.length - 1) {
      historyIndex++;
      inputEl.value = history[history.length - 1 - historyIndex];
    }
    return;
  }
  if (e.key === 'ArrowDown') {
    e.preventDefault();
    if (historyIndex > 0) {
      historyIndex--;
      inputEl.value = history[history.length - 1 - historyIndex];
    } else {
      historyIndex = -1;
      inputEl.value = '';
    }
    return;
  }
  if (e.key === 'Enter') {
    var val = inputEl.value;
    inputEl.value = '';
    if (val.trim()) {
      history.push(val);
    }
    historyIndex = -1;
    handleInput(val);
  }
});

document.getElementById('console-terminal').addEventListener('click', function() {
  inputEl.focus();
});

render();

// --- Power chart ---
var ctx = chartEl.getContext('2d');
var dpr = window.devicePixelRatio || 1;

function sizeCanvas() {
  var rect = chartEl.getBoundingClientRect();
  chartEl.width = rect.width * dpr;
  chartEl.height = rect.height * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}
sizeCanvas();
window.addEventListener('resize', function() { sizeCanvas(); drawChart(); });

function drawChart() {
  var w = chartEl.width / dpr;
  var h = chartEl.height / dpr;
  var pad = { top: 20, right: 20, bottom: 30, left: 50 };
  var plotW = w - pad.left - pad.right;
  var plotH = h - pad.top - pad.bottom;

  var maxY = 0;
  for (var i = 0; i < powerHistory.length; i++) {
    if (powerHistory[i] > maxY) maxY = powerHistory[i];
  }
  maxY = Math.max(maxY * 1.2, 15);

  ctx.clearRect(0, 0, w, h);

  ctx.strokeStyle = '#555';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pad.left, pad.top);
  ctx.lineTo(pad.left, pad.top + plotH);
  ctx.lineTo(pad.left + plotW, pad.top + plotH);
  ctx.stroke();

  ctx.fillStyle = '#aaa';
  ctx.font = '11px monospace';
  ctx.textAlign = 'right';
  var yTicks = 5;
  for (var t = 0; t <= yTicks; t++) {
    var val = (maxY / yTicks) * t;
    var y = pad.top + plotH - (val / maxY) * plotH;
    ctx.fillText(Math.round(val) + 'W', pad.left - 5, y + 4);
    ctx.strokeStyle = '#333';
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(pad.left + plotW, y);
    ctx.stroke();
  }

  ctx.textAlign = 'center';
  ctx.fillStyle = '#aaa';
  ctx.fillText('Power consumption (last 60s)', w / 2, h - 2);

  ctx.strokeStyle = '#0f0';
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (var i = 0; i < powerHistory.length; i++) {
    var x = pad.left + (i / (CHART_POINTS - 1)) * plotW;
    var y = pad.top + plotH - (powerHistory[i] / maxY) * plotH;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();
}

drawChart();

setInterval(function() {
  var noise = (Math.random() - 0.5) * 1.0;
  var sample = STATIC_POWER + currentPower + noise;
  if (sample < 0) sample = 0;
  powerHistory.push(sample);
  if (powerHistory.length > CHART_POINTS) powerHistory.shift();
  drawChart();
}, CHART_INTERVAL);

})();
