(function () {
  var root = document.getElementById('timeline-root');
  if (!root) return;
  var EVENTS = (window.TIMELINE_EVENTS || []).filter(function (e) {
    return e && e.year && e.year > 0;
  });

  var COLORS = {
    publication: '#2f6fed',
    artifact: '#8b3fd6',
    talk: '#f2c200',
    service: '#f08a24',
    teaching: '#e23b3b',
    other: '#9aa0a6'
  };
  var CATLABEL = {
    publication: 'Publications',
    artifact: 'Artifacts',
    talk: 'Talks',
    service: 'Service',
    teaching: 'Teaching',
    other: 'Others'
  };
  var ORDER = ['publication', 'artifact', 'talk', 'service', 'teaching', 'other'];
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var RANGE_PALETTE = ['#1f9e89', '#c0559f', '#3a86ff', '#e07a3f', '#5d8a3a', '#8a6fd6'];

  function parseIdx(s) {
    if (!s) return null;
    var p = String(s).split('-');
    var yr = parseInt(p[0], 10);
    var mo = parseInt(p[1], 10) || 1;
    if (!yr) return null;
    return yr * 12 + (mo - 1);
  }
  var RANGES = (window.TIMELINE_RANGES || []).map(function (r, i) {
    var s = parseIdx(r.start);
    var e = parseIdx(r.end);
    var ongoing = (e === null);
    return {
      label: r.label || '',
      color: r.color || RANGE_PALETTE[i % RANGE_PALETTE.length],
      detail: r.detail || '',
      startStr: r.start || '',
      endStr: r.end || '',
      startIdx: s,
      endIdx: e,
      ongoing: ongoing
    };
  }).filter(function (r) {
    return r.startIdx !== null;
  });

  function idxLabel(idx) {
    return MONTHS[idx % 12] + ' ' + Math.floor(idx / 12);
  }

  // ----- Legend -----
  var legend = document.createElement('div');
  legend.className = 'tl-legend';
  ORDER.forEach(function (c) {
    var item = document.createElement('span');
    item.className = 'tl-leg';
    var sw = document.createElement('span');
    sw.className = 'tl-swatch';
    sw.style.background = COLORS[c];
    var tx = document.createElement('span');
    tx.textContent = CATLABEL[c];
    item.appendChild(sw);
    item.appendChild(tx);
    legend.appendChild(item);
  });
  RANGES.forEach(function (r) {
    var item = document.createElement('span');
    item.className = 'tl-leg tl-leg-range';
    var sw = document.createElement('span');
    sw.className = 'tl-swatch-range';
    sw.style.borderTopColor = r.color;
    var tx = document.createElement('span');
    tx.textContent = r.label;
    item.appendChild(sw);
    item.appendChild(tx);
    legend.appendChild(item);
  });
  root.appendChild(legend);

  if (!EVENTS.length) {
    var empty = document.createElement('p');
    empty.textContent = 'No events to display.';
    root.appendChild(empty);
    return;
  }

  // ----- Group events by absolute month index (year*12 + month-1) -----
  var groups = {};
  EVENTS.forEach(function (e) {
    var idx = e.year * 12 + ((e.month || 1) - 1);
    (groups[idx] = groups[idx] || []).push(e);
  });
  Object.keys(groups).forEach(function (k) {
    groups[k].sort(function (a, b) {
      return ORDER.indexOf(a.cat) - ORDER.indexOf(b.cat);
    });
  });
  var idxs = Object.keys(groups).map(Number);
  var maxIdx = Math.max.apply(null, idxs);
  var minIdx = Math.min.apply(null, idxs);

  // Extend the timeline so every range is fully visible.
  RANGES.forEach(function (r) {
    maxIdx = Math.max(maxIdx, r.startIdx);
    minIdx = Math.min(minIdx, r.startIdx);
    if (!r.ongoing) {
      maxIdx = Math.max(maxIdx, r.endIdx);
      minIdx = Math.min(minIdx, r.endIdx);
    }
  });
  // Ongoing ranges run all the way to the top of the timeline (incl. future dates).
  RANGES.forEach(function (r) {
    if (r.ongoing) r.endIdx = maxIdx;
  });

  var monthY = {};

  // ----- Build the axis (newest on top) -----
  var axis = document.createElement('div');
  axis.className = 'tl-axis';
  var line = document.createElement('div');
  line.className = 'tl-line';
  axis.appendChild(line);

  var TOP = 30;
  var EMPTY_MONTH = 16;
  var YEAR_BLOCK = 36;
  var YEAR_GAP = 26;
  var MONTH_LABEL = 24;
  var ROW = 54;

  var y = TOP;
  var lastYear = null;
  var side = 0;

  for (var idx = maxIdx; idx >= minIdx; idx--) {
    var yr = Math.floor(idx / 12);
    var mo = (idx % 12) + 1;
    var ev = groups[idx];
    monthY[idx] = y;

    if (yr !== lastYear) {
      if (lastYear !== null) y += YEAR_GAP;
      var ym = document.createElement('div');
      ym.className = 'tl-year';
      ym.textContent = yr;
      ym.style.top = y + 'px';
      axis.appendChild(ym);
      y += YEAR_BLOCK;
      lastYear = yr;
    }

    if (ev && ev.length) {
      var ml = document.createElement('div');
      ml.className = 'tl-month';
      ml.textContent = MONTHS[mo - 1];
      ml.style.top = y + 'px';
      axis.appendChild(ml);
      y += MONTH_LABEL;

      ev.forEach(function (e) {
        var ey = y + ROW / 2;
        var isRight = (side % 2 === 0);
        side++;

        var dot = document.createElement('div');
        dot.className = 'tl-dot';
        dot.style.top = ey + 'px';
        dot.style.background = COLORS[e.cat] || COLORS.other;
        axis.appendChild(dot);

        var card = document.createElement('div');
        card.className = 'tl-card ' + (isRight ? 'tl-right' : 'tl-left');
        card.style.top = ey + 'px';
        card.setAttribute('tabindex', '0');

        var lab = document.createElement('div');
        lab.className = 'tl-label';
        lab.textContent = e.label || e.title || '';
        card.appendChild(lab);

        var det = document.createElement('div');
        det.className = 'tl-detail';

        var t = document.createElement('div');
        t.className = 'tl-title';
        t.textContent = e.title || e.label || '';
        det.appendChild(t);

        if (e.detail) {
          var d = document.createElement('div');
          d.className = 'tl-desc';
          d.textContent = e.detail;
          det.appendChild(d);
        }

        var dt = document.createElement('div');
        dt.className = 'tl-date';
        dt.textContent = MONTHS[mo - 1] + ' ' + yr;
        det.appendChild(dt);

        if (e.link) {
          var a = document.createElement('a');
          a.className = 'tl-link';
          a.href = e.link;
          a.textContent = 'Open';
          if (/^https?:/i.test(e.link)) {
            a.target = '_blank';
            a.rel = 'noopener';
          }
          det.appendChild(a);
        }

        card.appendChild(det);

        card.addEventListener('click', function (evt) {
          if (evt.target && evt.target.classList.contains('tl-link')) return;
          var wasOpen = this.classList.contains('open');
          closeAll();
          if (!wasOpen) this.classList.add('open');
        });

        axis.appendChild(card);
        y += ROW;
      });

      y += 8;
    } else {
      y += EMPTY_MONTH;
    }
  }

  monthY[minIdx - 1] = y;
  axis.style.height = (y + TOP) + 'px';

  // ----- Range "era" lines (parallel dashed lines, one lane per overlap) -----
  var LANE_PAD = 6;
  var LANE_W = 30;
  var sortedRanges = RANGES.slice().sort(function (a, b) {
    return a.startIdx - b.startIdx;
  });
  var laneEnds = [];
  sortedRanges.forEach(function (r) {
    var placed = false;
    for (var li = 0; li < laneEnds.length; li++) {
      if (r.startIdx > laneEnds[li]) {
        r.lane = li;
        laneEnds[li] = r.endIdx;
        placed = true;
        break;
      }
    }
    if (!placed) {
      r.lane = laneEnds.length;
      laneEnds.push(r.endIdx);
    }
  });

  RANGES.forEach(function (r) {
    var topY = monthY[r.endIdx];
    var botY = monthY[r.startIdx - 1];
    if (topY == null || botY == null) return;
    var h = Math.max(botY - topY, 4);

    var el = document.createElement('div');
    el.className = 'tl-range' + (r.ongoing ? ' tl-range-ongoing' : '');
    el.style.top = topY + 'px';
    el.style.height = h + 'px';
    el.style.left = (LANE_PAD + r.lane * LANE_W) + 'px';
    el.style.setProperty('--rc', r.color);
    el.setAttribute('tabindex', '0');

    var lab = document.createElement('div');
    lab.className = 'tl-range-label';
    lab.textContent = r.label;
    el.appendChild(lab);

    var det = document.createElement('div');
    det.className = 'tl-range-detail';
    var t = document.createElement('div');
    t.className = 'tl-title';
    t.textContent = r.label;
    det.appendChild(t);
    var period = document.createElement('div');
    period.className = 'tl-date';
    period.textContent = r.ongoing
      ? ('Since ' + idxLabel(r.startIdx))
      : (idxLabel(r.startIdx) + ' \u2013 ' + idxLabel(r.endIdx));
    det.appendChild(period);
    if (r.detail) {
      var d = document.createElement('div');
      d.className = 'tl-desc';
      d.textContent = r.detail;
      det.appendChild(d);
    }
    el.appendChild(det);

    el.addEventListener('click', function () {
      var wasOpen = this.classList.contains('open');
      closeAll();
      if (!wasOpen) this.classList.add('open');
    });

    axis.appendChild(el);
  });

  root.appendChild(axis);

  function closeAll() {
    var open = axis.querySelectorAll('.tl-card.open, .tl-range.open');
    for (var i = 0; i < open.length; i++) open[i].classList.remove('open');
  }
  document.addEventListener('click', function (evt) {
    if (!evt.target.closest || !(evt.target.closest('.tl-card') || evt.target.closest('.tl-range'))) closeAll();
  });

  // ----- Scroll arrow buttons -----
  var btns = document.createElement('div');
  btns.className = 'tl-scroll-btns';
  var up = document.createElement('button');
  up.type = 'button';
  up.className = 'tl-scroll-btn';
  up.setAttribute('aria-label', 'Scroll up');
  up.textContent = '\u2191';
  var down = document.createElement('button');
  down.type = 'button';
  down.className = 'tl-scroll-btn';
  down.setAttribute('aria-label', 'Scroll down');
  down.textContent = '\u2193';
  btns.appendChild(up);
  btns.appendChild(down);
  document.body.appendChild(btns);

  function step(dir) {
    window.scrollBy({ top: dir * window.innerHeight * 0.85, left: 0, behavior: 'smooth' });
  }
  up.addEventListener('click', function () { step(-1); });
  down.addEventListener('click', function () { step(1); });
})();
