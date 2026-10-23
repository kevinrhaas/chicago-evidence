/* @ds-bundle: {"format":4,"namespace":"Chicago4DTemporalObservatory_8fcc19","components":[{"name":"BrandMark","sourcePath":"components/brand/BrandMark.jsx"},{"name":"Masthead","sourcePath":"components/brand/Masthead.jsx"},{"name":"EngageButton","sourcePath":"components/controls/EngageButton.jsx"},{"name":"MACHINES","sourcePath":"components/controls/MachineSelector.jsx"},{"name":"MachineSelector","sourcePath":"components/controls/MachineSelector.jsx"},{"name":"Pill","sourcePath":"components/controls/Pill.jsx"},{"name":"SearchField","sourcePath":"components/controls/SearchField.jsx"},{"name":"Tabs","sourcePath":"components/controls/Tabs.jsx"},{"name":"Toggle","sourcePath":"components/controls/Toggle.jsx"},{"name":"EraArt","sourcePath":"components/destinations/EraArt.jsx"},{"name":"EraCard","sourcePath":"components/destinations/EraCard.jsx"},{"name":"SectionLine","sourcePath":"components/destinations/SectionLine.jsx"},{"name":"AcquisitionStatus","sourcePath":"components/instruments/AcquisitionStatus.jsx"},{"name":"Chronometer","sourcePath":"components/instruments/Chronometer.jsx"},{"name":"IndicatorLamp","sourcePath":"components/instruments/IndicatorLamp.jsx"},{"name":"Placard","sourcePath":"components/instruments/Placard.jsx"},{"name":"Telemetry","sourcePath":"components/instruments/Telemetry.jsx"},{"name":"TransitSequence","sourcePath":"components/instruments/TransitSequence.jsx"},{"name":"YearReadout","sourcePath":"components/instruments/YearReadout.jsx"},{"name":"DepartureOverlay","sourcePath":"components/overlays/DepartureOverlay.jsx"},{"name":"BuildingCard","sourcePath":"components/records/BuildingCard.jsx"},{"name":"ConfidenceGrade","sourcePath":"components/records/ConfidenceGrade.jsx"},{"name":"ResultRow","sourcePath":"components/records/ResultRow.jsx"},{"name":"ResultGroup","sourcePath":"components/records/ResultRow.jsx"}],"sourceHashes":{"components/brand/BrandMark.jsx":"83d90a5d8d0a","components/brand/Masthead.jsx":"a944e31fc697","components/controls/EngageButton.jsx":"5868f825ca58","components/controls/MachineSelector.jsx":"e007571102b8","components/controls/Pill.jsx":"4dbe61de3e3f","components/controls/SearchField.jsx":"bd6847e76f9b","components/controls/Tabs.jsx":"4c6ecb0bbaef","components/controls/Toggle.jsx":"a5cb377f4e21","components/destinations/EraArt.jsx":"68af88ae46ef","components/destinations/EraCard.jsx":"d2ca612628b4","components/destinations/SectionLine.jsx":"8db8c3e97b3d","components/instruments/AcquisitionStatus.jsx":"5e5f9f58ec49","components/instruments/Chronometer.jsx":"9eed684f9cd7","components/instruments/IndicatorLamp.jsx":"454a9e037932","components/instruments/Placard.jsx":"c0bff7dc96c8","components/instruments/Telemetry.jsx":"487fc2dea1dc","components/instruments/TransitSequence.jsx":"13809a43f9c0","components/instruments/YearReadout.jsx":"f0630006f4fe","components/overlays/DepartureOverlay.jsx":"23f939a75f59","components/records/BuildingCard.jsx":"0b301c228409","components/records/ConfidenceGrade.jsx":"11a43d7ba0db","components/records/ResultRow.jsx":"803a3723c014","dev/bundle-fallback.js":"105060f2ae4f","ui_kits/observatory/Arrival.jsx":"607cd02fec5b","ui_kits/observatory/Briefing.jsx":"e9cbe651ca06","ui_kits/observatory/Home.jsx":"ec97c2467691","ui_kits/observatory/Pending.jsx":"4c06b710063b"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.Chicago4DTemporalObservatory_8fcc19 = window.Chicago4DTemporalObservatory_8fcc19 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/brand/BrandMark.jsx
try { (() => {
function BrandMark({
  size = 28,
  code = '4D',
  name = 'CHICAGO',
  href,
  showWordmark = true
}) {
  const Tag = href ? 'a' : 'span';
  return /*#__PURE__*/React.createElement(Tag, {
    className: "c4d-brand",
    href: href,
    "aria-label": "Chicago 4D"
  }, /*#__PURE__*/React.createElement("svg", {
    className: "c4d-brand-mark",
    "aria-hidden": "true",
    width: size,
    height: size,
    viewBox: "0 0 32 32"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "16",
    cy: "16",
    r: "14",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M29 16H17L7 6M17 16L7 26",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.5"
  })), showWordmark && /*#__PURE__*/React.createElement("span", null, name, code && /*#__PURE__*/React.createElement("b", null, code)));
}
Object.assign(__ds_scope, { BrandMark });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/BrandMark.jsx", error: String((e && e.message) || e) }); }

// components/brand/Masthead.jsx
try { (() => {
function Masthead({
  station = 'Temporal Observatory',
  status = 'Online',
  href = '#',
  children
}) {
  return /*#__PURE__*/React.createElement("header", {
    className: "c4d-masthead"
  }, /*#__PURE__*/React.createElement(__ds_scope.BrandMark, {
    href: href
  }), /*#__PURE__*/React.createElement("div", {
    className: "c4d-masthead-right"
  }, /*#__PURE__*/React.createElement("span", {
    className: "c4d-station"
  }, station, /*#__PURE__*/React.createElement("i", null), status), children));
}
Object.assign(__ds_scope, { Masthead });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/brand/Masthead.jsx", error: String((e && e.message) || e) }); }

// components/controls/EngageButton.jsx
try { (() => {
function EngageButton({
  children = 'Engage',
  variant = 'primary',
  size = 'md',
  arrow = false,
  disabled = false,
  href,
  onClick,
  type = 'button'
}) {
  const Tag = href ? 'a' : 'button';
  return /*#__PURE__*/React.createElement(Tag, {
    className: "c4d-btn",
    "data-variant": variant,
    "data-size": size,
    href: href,
    onClick: onClick,
    disabled: Tag === 'button' ? disabled : undefined,
    "aria-disabled": disabled || undefined,
    type: Tag === 'button' ? type : undefined
  }, children, arrow && /*#__PURE__*/React.createElement("span", {
    className: "c4d-btn-arrow",
    "aria-hidden": "true"
  }, "\u2192"));
}
Object.assign(__ds_scope, { EngageButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/controls/EngageButton.jsx", error: String((e && e.message) || e) }); }

// components/controls/MachineSelector.jsx
try { (() => {
const MACHINES = [{
  id: 'control-room',
  name: '1960s Control Room',
  code: 'CR-61',
  swatch: ['#ECE6D8', '#1E3A66', '#D6352B', '#8CF5A8']
}, {
  id: 'brass',
  name: 'Precision Brass',
  code: 'PB-1888',
  swatch: ['#F4E6CD', '#D4A85A', '#3A2416', '#3F8F7F']
}, {
  id: 'worlds-fair',
  name: "World's Fair",
  code: 'WF-33',
  swatch: ['#EFE9DC', '#138A92', '#EC6A1E', '#363A3B']
}, {
  id: 'deep-space',
  name: 'Deep Space',
  code: 'DS-∞',
  swatch: ['#E4E2DC', '#7AD7F6', '#F5A742', '#07090C']
}];
function MachineSelector({
  value = 'control-room',
  onChange,
  compact = false,
  machines = MACHINES
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-machines",
    "data-compact": String(compact),
    role: "group",
    "aria-label": "Machine",
    style: {
      '--cols': machines.length
    }
  }, machines.map(m => /*#__PURE__*/React.createElement("button", {
    key: m.id,
    type: "button",
    className: "c4d-machine",
    "aria-pressed": value === m.id,
    onClick: () => onChange && onChange(m.id),
    title: m.name
  }, /*#__PURE__*/React.createElement("span", {
    className: "c4d-machine-swatch"
  }, m.swatch.map(c => /*#__PURE__*/React.createElement("span", {
    key: c,
    style: {
      background: c
    }
  }))), /*#__PURE__*/React.createElement("span", {
    className: "c4d-machine-name"
  }, m.name), /*#__PURE__*/React.createElement("span", {
    className: "c4d-machine-code"
  }, /*#__PURE__*/React.createElement("span", null, m.code), /*#__PURE__*/React.createElement("span", null, value === m.id ? 'Engaged' : 'Standby')))));
}
Object.assign(__ds_scope, { MACHINES, MachineSelector });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/controls/MachineSelector.jsx", error: String((e && e.message) || e) }); }

// components/controls/Pill.jsx
try { (() => {
function Pill({
  children,
  pressed = false,
  count,
  disabled = false,
  onClick
}) {
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "c4d-pill",
    "aria-pressed": pressed,
    disabled: disabled,
    onClick: onClick
  }, children, count != null && /*#__PURE__*/React.createElement("span", {
    className: "c4d-pill-n"
  }, count));
}
Object.assign(__ds_scope, { Pill });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/controls/Pill.jsx", error: String((e && e.message) || e) }); }

// components/controls/SearchField.jsx
try { (() => {
function SearchField({
  value,
  onChange,
  placeholder = 'Search the 1835 register…',
  label = 'Search'
}) {
  return /*#__PURE__*/React.createElement("label", {
    className: "c4d-search"
  }, /*#__PURE__*/React.createElement("svg", {
    width: "14",
    height: "14",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "11",
    cy: "11",
    r: "7"
  }), /*#__PURE__*/React.createElement("path", {
    d: "m20 20-3.5-3.5"
  })), /*#__PURE__*/React.createElement("input", {
    type: "search",
    "aria-label": label,
    value: value,
    onChange: e => onChange && onChange(e.target.value),
    placeholder: placeholder
  }));
}
Object.assign(__ds_scope, { SearchField });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/controls/SearchField.jsx", error: String((e && e.message) || e) }); }

// components/controls/Tabs.jsx
try { (() => {
function Tabs({
  tabs = [],
  value,
  onChange
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-tabs",
    role: "tablist"
  }, tabs.map(t => /*#__PURE__*/React.createElement("button", {
    key: t.id,
    role: "tab",
    type: "button",
    className: "c4d-tab",
    "aria-selected": value === t.id,
    onClick: () => onChange && onChange(t.id)
  }, t.label, t.count != null && /*#__PURE__*/React.createElement("span", {
    className: "c4d-tab-count"
  }, t.count))));
}
Object.assign(__ds_scope, { Tabs });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/controls/Tabs.jsx", error: String((e && e.message) || e) }); }

// components/controls/Toggle.jsx
try { (() => {
function Toggle({
  label,
  checked = false,
  onChange,
  detail
}) {
  return /*#__PURE__*/React.createElement("label", {
    className: "c4d-toggle"
  }, /*#__PURE__*/React.createElement("input", {
    type: "checkbox",
    checked: checked,
    onChange: e => onChange && onChange(e.target.checked)
  }), /*#__PURE__*/React.createElement("span", {
    className: "c4d-toggle-track",
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("span", null, label, detail != null && /*#__PURE__*/React.createElement(React.Fragment, null, " ", /*#__PURE__*/React.createElement("b", null, detail))));
}
Object.assign(__ds_scope, { Toggle });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/controls/Toggle.jsx", error: String((e && e.message) || e) }); }

// components/destinations/EraArt.jsx
try { (() => {
const PATHS = {
  town: 'M0 88H400M24 88V52L49 34L74 52V88M83 88V62L110 45L139 62V88M154 88V40L179 20L204 40V88M222 88V54L251 32L280 54V88M303 88V58L340 39L379 58V88M40 67H58M98 73H118M169 53H188M242 68H261M326 74H351M190 28V9H198V35',
  avenue: 'M0 88H400M30 88V39L56 22L83 39V88M90 88V27H107V19H178V27H194V88M114 88V40H170V88M208 88V45L244 16L282 45V88M225 88V61H264V88M300 88V33L341 13L382 33V88M318 46H333V62H318ZM352 46H367V62H352ZM44 46H67V68H44ZM128 52H152V68H128Z',
  shore: 'M0 88Q50 76 97 88T192 88T289 88T400 88M23 70Q70 57 104 70M260 71Q310 61 375 70M118 83V40L137 29L157 40V83M157 78H239V42L258 29L277 42V84M162 45V76M173 45V76M184 45V76M195 45V76M206 45V76M217 45V76M228 45V76M133 28V9H160L133 17'
};
function EraArt({
  kind = 'town'
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-era-art",
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 400 100",
    preserveAspectRatio: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: PATHS[kind] || PATHS.town
  })));
}
Object.assign(__ds_scope, { EraArt });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/destinations/EraArt.jsx", error: String((e && e.message) || e) }); }

// components/destinations/EraCard.jsx
try { (() => {
function EraCard({
  index = '01',
  name = 'River settlement',
  year = '1835',
  title = 'At the river’s forks',
  body,
  state = 'Coordinate locked',
  pending = false,
  primary = false,
  imageSrc,
  art = 'town',
  footLeft = 'Summer · July 1',
  footRight = 'Engage',
  href,
  onClick
}) {
  const Tag = href ? 'a' : 'div';
  return /*#__PURE__*/React.createElement(Tag, {
    className: "c4d-era",
    href: href,
    onClick: onClick,
    "data-primary": String(primary),
    "data-pending": String(pending),
    role: href ? undefined : 'button',
    tabIndex: href ? undefined : 0,
    "data-year": year
  }, /*#__PURE__*/React.createElement("div", {
    className: "c4d-era-top"
  }, /*#__PURE__*/React.createElement("span", null, index, " / ", name), /*#__PURE__*/React.createElement("span", {
    className: "c4d-era-state"
  }, /*#__PURE__*/React.createElement("i", null), state)), imageSrc ? /*#__PURE__*/React.createElement("div", {
    className: "c4d-era-plate"
  }, /*#__PURE__*/React.createElement("img", {
    src: imageSrc,
    alt: ""
  })) : /*#__PURE__*/React.createElement(__ds_scope.EraArt, {
    kind: art
  }), /*#__PURE__*/React.createElement("div", {
    className: "c4d-era-body"
  }, /*#__PURE__*/React.createElement("div", {
    className: "c4d-era-title"
  }, /*#__PURE__*/React.createElement("span", {
    className: "c4d-era-year"
  }, year), /*#__PURE__*/React.createElement("span", {
    className: "c4d-era-arrow",
    "aria-hidden": "true"
  }, "\u2197")), /*#__PURE__*/React.createElement("h3", null, title), body && /*#__PURE__*/React.createElement("p", null, body)), /*#__PURE__*/React.createElement("div", {
    className: "c4d-era-foot"
  }, /*#__PURE__*/React.createElement("span", null, footLeft), /*#__PURE__*/React.createElement("span", null, footRight, " ", /*#__PURE__*/React.createElement("b", {
    "aria-hidden": "true"
  }, "\u2192"))));
}
Object.assign(__ds_scope, { EraCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/destinations/EraCard.jsx", error: String((e && e.message) || e) }); }

// components/destinations/SectionLine.jsx
try { (() => {
function SectionLine({
  title,
  meta,
  metaValue,
  children
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-section-line"
  }, /*#__PURE__*/React.createElement("h2", null, title), children || meta && /*#__PURE__*/React.createElement("span", null, meta, metaValue != null && /*#__PURE__*/React.createElement("b", null, metaValue)));
}
Object.assign(__ds_scope, { SectionLine });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/destinations/SectionLine.jsx", error: String((e && e.message) || e) }); }

// components/instruments/AcquisitionStatus.jsx
try { (() => {
function AcquisitionStatus({
  message = 'Three coordinates locked. Field nominal.',
  count = '03 / 03',
  busy = false
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-acq",
    "data-busy": String(busy)
  }, /*#__PURE__*/React.createElement("span", {
    className: "c4d-acq-signal",
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("p", {
    role: "status"
  }, message), count && /*#__PURE__*/React.createElement("span", {
    className: "c4d-acq-count",
    "aria-hidden": "true"
  }, count));
}
Object.assign(__ds_scope, { AcquisitionStatus });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/instruments/AcquisitionStatus.jsx", error: String((e && e.message) || e) }); }

// components/instruments/Chronometer.jsx
try { (() => {
function Chronometer({
  phase = 'scan',
  size = 420,
  note = 'The river is the constant',
  imageSrc,
  label = ['CHICAGO · TEMPORAL FIELD / ', 'WOLF POINT APERTURE / ']
}) {
  const id = React.useId ? React.useId().replace(/:/g, '') : 'c4d';
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-chrono",
    "data-phase": phase,
    style: {
      '--chrono-size': size + 'px'
    },
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 520 520"
  }, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("radialGradient", {
    id: id + 'core'
  }, /*#__PURE__*/React.createElement("stop", {
    stopColor: "currentColor",
    stopOpacity: ".15"
  }), /*#__PURE__*/React.createElement("stop", {
    offset: "1",
    stopColor: "currentColor",
    stopOpacity: "0"
  })), /*#__PURE__*/React.createElement("path", {
    id: id + 'orbit',
    d: "M 260,55 A 205,205 0 1,1 259.9,55"
  })), /*#__PURE__*/React.createElement("circle", {
    cx: "260",
    cy: "260",
    r: "235",
    fill: 'url(#' + id + 'core)'
  }), /*#__PURE__*/React.createElement("g", {
    className: "orbit slow"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "260",
    cy: "260",
    r: "225",
    className: "hair"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "260",
    cy: "260",
    r: "219",
    className: "ticks"
  }), /*#__PURE__*/React.createElement("text", {
    className: "orbit-label"
  }, /*#__PURE__*/React.createElement("textPath", {
    href: '#' + id + 'orbit',
    startOffset: "0%"
  }, label[0]), /*#__PURE__*/React.createElement("textPath", {
    href: '#' + id + 'orbit',
    startOffset: "50%"
  }, label[1]))), /*#__PURE__*/React.createElement("g", {
    className: "orbit reverse"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "260",
    cy: "260",
    r: "181",
    className: "hair"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "260",
    cy: "260",
    r: "176",
    className: "segments"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "83",
    cy: "260",
    r: "4",
    className: "dot"
  })), /*#__PURE__*/React.createElement("circle", {
    cx: "260",
    cy: "260",
    r: "143",
    className: "hair"
  }), /*#__PURE__*/React.createElement("path", {
    className: "crosshair",
    d: "M260 20V102M260 418V500M20 260H102M418 260H500"
  }), phase !== 'arrive' && /*#__PURE__*/React.createElement("g", {
    className: "sweep"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M260 260L260 84A176 176 0 0 1 384 135Z"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "260",
    y1: "260",
    x2: "384",
    y2: "135"
  })), /*#__PURE__*/React.createElement("g", {
    className: "river"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M389 260H265Q250 260 239 246L153 139M254 258Q242 283 225 302L146 385"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M394 273H271Q253 273 245 288L161 392M254 249L166 132"
  })), /*#__PURE__*/React.createElement("circle", {
    cx: "260",
    cy: "260",
    r: "62",
    className: "hair"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "260",
    cy: "260",
    r: "8",
    className: "dot"
  }), /*#__PURE__*/React.createElement("path", {
    className: "crosshair",
    d: "M235 260H246M274 260H285M260 235V246M260 274V285"
  }), /*#__PURE__*/React.createElement("g", {
    className: "orbit"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "260",
    cy: "84",
    r: "7",
    className: "beacon"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "411",
    cy: "349",
    r: "5",
    className: "beacon"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "109",
    cy: "349",
    r: "5",
    className: "beacon"
  })), phase === 'lock' && /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("circle", {
    cx: "196",
    cy: "182",
    r: "16",
    className: "lock"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "196",
    cy: "182",
    r: "5",
    className: "lock-dot"
  }), /*#__PURE__*/React.createElement("path", {
    className: "lock",
    d: "M196 156V166M196 198V208M170 182H180M212 182H222"
  }))), phase === 'arrive' && imageSrc && /*#__PURE__*/React.createElement("div", {
    className: "c4d-chrono-arrive"
  }, /*#__PURE__*/React.createElement("img", {
    src: imageSrc,
    alt: ""
  })), note && /*#__PURE__*/React.createElement("span", {
    className: "c4d-chrono-note"
  }, note));
}
Object.assign(__ds_scope, { Chronometer });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/instruments/Chronometer.jsx", error: String((e && e.message) || e) }); }

// components/instruments/IndicatorLamp.jsx
try { (() => {
const TONES = {
  lamp: 'var(--lamp)',
  accent: 'var(--accent)',
  signal: 'var(--signal)',
  alert: 'var(--alert)',
  ok: 'var(--ok)'
};
function IndicatorLamp({
  label,
  on = true,
  blink = false,
  tone = 'lamp',
  size = 9
}) {
  return /*#__PURE__*/React.createElement("span", {
    className: "c4d-lamp",
    "data-on": String(on),
    "data-blink": String(blink),
    style: {
      '--lamp-c': TONES[tone] || tone,
      '--lamp-size': size + 'px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "c4d-lamp-bulb"
  }), label);
}
Object.assign(__ds_scope, { IndicatorLamp });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/instruments/IndicatorLamp.jsx", error: String((e && e.message) || e) }); }

// components/instruments/Placard.jsx
try { (() => {
function Placard({
  title = 'Interval field',
  note = 'Authorized personnel · Circle-3 clearance',
  glyph = '☢',
  tone = 'solid'
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-placard",
    "data-tone": tone,
    role: "note"
  }, tone !== 'stripe' && /*#__PURE__*/React.createElement("span", {
    className: "c4d-placard-glyph",
    "aria-hidden": "true"
  }, glyph), /*#__PURE__*/React.createElement("span", {
    className: "c4d-placard-body"
  }, title, note && /*#__PURE__*/React.createElement("small", null, note)));
}
Object.assign(__ds_scope, { Placard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/instruments/Placard.jsx", error: String((e && e.message) || e) }); }

// components/instruments/Telemetry.jsx
try { (() => {
function Telemetry({
  items = []
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-telemetry"
  }, items.map(it => /*#__PURE__*/React.createElement("div", {
    key: it.label,
    className: "c4d-telemetry-cell",
    "data-state": it.state || 'normal'
  }, /*#__PURE__*/React.createElement("span", {
    className: "c4d-label"
  }, it.label), /*#__PURE__*/React.createElement("b", null, it.value))));
}
Object.assign(__ds_scope, { Telemetry });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/instruments/Telemetry.jsx", error: String((e && e.message) || e) }); }

// components/instruments/TransitSequence.jsx
try { (() => {
function TransitSequence({
  steps = ['Scan', 'Lock', 'Arrive'],
  current = 0
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-seq",
    role: "list"
  }, steps.map((s, i) => {
    const state = i < current ? 'done' : i === current ? 'current' : 'pending';
    const lampStyle = {
      '--lamp-c': i === current ? 'var(--signal)' : 'var(--accent)'
    };
    return /*#__PURE__*/React.createElement(React.Fragment, {
      key: s
    }, i > 0 && /*#__PURE__*/React.createElement("span", {
      className: "c4d-seq-sep",
      "aria-hidden": "true"
    }, "\u203A"), /*#__PURE__*/React.createElement("span", {
      className: "c4d-seq-step",
      role: "listitem",
      "data-state": state
    }, /*#__PURE__*/React.createElement("span", {
      className: "c4d-lamp",
      "data-on": String(i <= current),
      "data-blink": String(i === current),
      style: lampStyle
    }, /*#__PURE__*/React.createElement("span", {
      className: "c4d-lamp-bulb"
    })), s));
  }));
}
Object.assign(__ds_scope, { TransitSequence });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/instruments/TransitSequence.jsx", error: String((e && e.message) || e) }); }

// components/instruments/YearReadout.jsx
try { (() => {
function YearReadout({
  year = '1835',
  label = 'Destination year',
  size = 44
}) {
  const digits = String(year).split('');
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-readout",
    style: {
      '--readout-size': size + 'px'
    }
  }, label && /*#__PURE__*/React.createElement("span", {
    className: "c4d-label"
  }, label), /*#__PURE__*/React.createElement("div", {
    className: "c4d-readout-digits",
    role: "img",
    "aria-label": label + ' ' + year
  }, digits.map((d, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    className: "c4d-readout-digit"
  }, d))));
}
Object.assign(__ds_scope, { YearReadout });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/instruments/YearReadout.jsx", error: String((e && e.message) || e) }); }

// components/overlays/DepartureOverlay.jsx
try { (() => {
function DepartureOverlay({
  year = '1835',
  eyebrow = 'Temporal transfer',
  message = 'Coordinate locked. Breaching the interval…',
  open = true,
  inline = false,
  onAbort,
  abortLabel = 'Abort transfer',
  children
}) {
  if (!open) return null;
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-depart",
    "data-inline": String(inline),
    role: "status",
    "aria-live": "polite"
  }, /*#__PURE__*/React.createElement("div", {
    className: "c4d-depart-ring",
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("p", {
    className: "c4d-depart-eyebrow"
  }, eyebrow), /*#__PURE__*/React.createElement("div", {
    className: "c4d-depart-year"
  }, year), /*#__PURE__*/React.createElement("p", null, message), (onAbort || children) && /*#__PURE__*/React.createElement("div", {
    className: "c4d-depart-actions"
  }, children, onAbort && /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "c4d-btn",
    "data-variant": "ghost",
    "data-size": "sm",
    onClick: onAbort
  }, abortLabel)));
}
Object.assign(__ds_scope, { DepartureOverlay });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/overlays/DepartureOverlay.jsx", error: String((e && e.message) || e) }); }

// components/records/BuildingCard.jsx
try { (() => {
const GRADE_VAR = {
  documented: 'var(--doc)',
  inferred: 'var(--inf)',
  conjectural: 'var(--con)'
};
function BuildingCard({
  title,
  aka,
  kind,
  where,
  flags = [],
  lead,
  facts = [],
  tabs,
  onClose,
  children
}) {
  const [tab, setTab] = React.useState(tabs && tabs[0] ? tabs[0].id : null);
  const active = tabs && tabs.find(t => t.id === tab);
  return /*#__PURE__*/React.createElement("article", {
    className: "c4d-card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "c4d-card-head"
  }, /*#__PURE__*/React.createElement("div", {
    className: "c4d-card-title"
  }, /*#__PURE__*/React.createElement("h2", null, title), onClose && /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "c4d-card-close",
    "aria-label": "Close",
    onClick: onClose
  }, "\xD7")), aka && /*#__PURE__*/React.createElement("p", {
    className: "c4d-card-aka"
  }, aka), kind && /*#__PURE__*/React.createElement("p", {
    className: "c4d-card-kind"
  }, kind), where && /*#__PURE__*/React.createElement("p", {
    className: "c4d-card-where"
  }, where), flags.length > 0 && /*#__PURE__*/React.createElement("div", {
    className: "c4d-card-flags"
  }, flags.map((f, i) => /*#__PURE__*/React.createElement("p", {
    key: i,
    className: "c4d-flag",
    "data-held": String(!!f.held)
  }, f.text)))), lead && /*#__PURE__*/React.createElement("p", {
    className: "c4d-card-lead"
  }, lead), facts.length > 0 && /*#__PURE__*/React.createElement("dl", {
    className: "c4d-facts"
  }, facts.map(f => /*#__PURE__*/React.createElement("div", {
    key: f.label,
    className: f.wide ? 'wide' : undefined
  }, /*#__PURE__*/React.createElement("dt", null, f.label), /*#__PURE__*/React.createElement("dd", null, f.value, f.grade && /*#__PURE__*/React.createElement("span", {
    className: "c4d-dot",
    style: {
      color: GRADE_VAR[f.grade]
    },
    title: f.grade
  }))))), tabs && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(__ds_scope.Tabs, {
    tabs: tabs,
    value: tab,
    onChange: setTab
  }), /*#__PURE__*/React.createElement("div", {
    className: "c4d-card-pane"
  }, active && active.content)), children);
}
Object.assign(__ds_scope, { BuildingCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/records/BuildingCard.jsx", error: String((e && e.message) || e) }); }

// components/records/ConfidenceGrade.jsx
try { (() => {
const G = {
  documented: 'var(--doc)',
  inferred: 'var(--inf)',
  conjectural: 'var(--con)'
};
const LABEL = {
  documented: 'Documented',
  inferred: 'Inferred',
  conjectural: 'Conjectural'
};
function ConfidenceGrade({
  grade = 'documented',
  label,
  chip = false,
  showLabel = true
}) {
  return /*#__PURE__*/React.createElement("span", {
    className: "c4d-grade",
    "data-grade": grade,
    "data-chip": String(chip),
    title: LABEL[grade],
    style: {
      '--g': G[grade]
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "c4d-dot"
  }), showLabel && (label || LABEL[grade]));
}
Object.assign(__ds_scope, { ConfidenceGrade });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/records/ConfidenceGrade.jsx", error: String((e && e.message) || e) }); }

// components/records/ResultRow.jsx
try { (() => {
function ResultRow({
  name,
  sub,
  distance,
  bearing = 0,
  grade,
  active = false,
  onClick
}) {
  const g = {
    documented: 'var(--doc)',
    inferred: 'var(--inf)',
    conjectural: 'var(--con)'
  }[grade];
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "c4d-row",
    "data-active": String(active),
    onClick: onClick
  }, /*#__PURE__*/React.createElement("span", {
    className: "c4d-row-main"
  }, /*#__PURE__*/React.createElement("span", {
    className: "c4d-row-name"
  }, name), sub && /*#__PURE__*/React.createElement("span", {
    className: "c4d-row-sub"
  }, sub)), /*#__PURE__*/React.createElement("span", {
    className: "c4d-row-side"
  }, distance && /*#__PURE__*/React.createElement("span", {
    className: "c4d-row-dist"
  }, /*#__PURE__*/React.createElement("span", {
    className: "c4d-row-arrow",
    style: {
      '--turn': bearing + 'deg'
    }
  }, "\u2191"), distance), g && /*#__PURE__*/React.createElement("span", {
    className: "c4d-dot",
    style: {
      color: g,
      margin: 0
    }
  })));
}
function ResultGroup({
  label,
  count
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "c4d-group"
  }, /*#__PURE__*/React.createElement("span", null, label), count != null && /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 500,
      letterSpacing: 0
    }
  }, count));
}
Object.assign(__ds_scope, { ResultRow, ResultGroup });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/records/ResultRow.jsx", error: String((e && e.message) || e) }); }

// dev/bundle-fallback.js
try { (() => {
/* Dev-only fallback: when _ds_bundle.js has not been compiled yet, transpile component sources in-browser. Consumers never need this. */
(function () {
  var NS = 'Chicago4DTemporalObservatory_8fcc19';
  if (window[NS]) return;
  var cur = document.currentScript.src;
  var root = cur.replace(/dev\/bundle-fallback\.js.*$/, '');
  var files = ["brand/BrandMark", "brand/Masthead", "instruments/Chronometer", "instruments/YearReadout", "instruments/IndicatorLamp", "instruments/TransitSequence", "instruments/AcquisitionStatus", "instruments/Telemetry", "instruments/Placard", "controls/Tabs", "controls/EngageButton", "controls/MachineSelector", "controls/Pill", "controls/SearchField", "controls/Toggle", "destinations/EraArt", "destinations/EraCard", "destinations/SectionLine", "records/ConfidenceGrade", "records/BuildingCard", "records/ResultRow", "overlays/DepartureOverlay"];
  var src = '';
  var names = [];
  files.forEach(function (f) {
    var x = new XMLHttpRequest();
    x.open('GET', root + 'components/' + f + '.jsx', false);
    x.send();
    var t = x.responseText.replace(/^import .*$/mg, '');
    t.replace(/export (?:function|const) ([A-Za-z0-9_]+)/g, function (m, n) {
      names.push(n);
    });
    src += t.replace(/export /g, '') + '\n';
  });
  src += 'window.' + NS + '={' + names.join(',') + '};';
  var out = Babel.transform(src, {
    presets: ['react']
  }).code;
  (0, eval)(out);
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "dev/bundle-fallback.js", error: String((e && e.message) || e) }); }

// ui_kits/observatory/Arrival.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const {
  BrandMark,
  Telemetry: ATelemetry,
  EngageButton: AButton,
  SectionLine: ASection,
  SearchField,
  Pill,
  Toggle,
  ResultGroup,
  ResultRow,
  BuildingCard,
  ConfidenceGrade
} = window.Chicago4DTemporalObservatory_8fcc19;
const STRUCTURES = [{
  id: 'sauganash',
  group: 'Taverns',
  name: 'Sauganash Hotel',
  sub: 'Lake St · Mark Beaubien',
  distance: '340 ft',
  bearing: 45,
  grade: 'documented',
  kind: 'Hotel · frame, two storeys',
  where: 'Lake Street at Market, east bank of the South Branch',
  lead: 'Beaubien’s house of entertainment — fiddle in the parlour, and the first theatre of the town in its dining room.',
  facts: [{
    label: 'Built',
    value: '1831',
    grade: 'documented'
  }, {
    label: 'Storeys',
    value: 'Two',
    grade: 'documented'
  }, {
    label: 'Roof',
    value: 'Gable, shingled',
    grade: 'inferred'
  }, {
    label: 'Paint',
    value: 'White, blue trim',
    grade: 'conjectural'
  }]
}, {
  id: 'greentree',
  group: 'Taverns',
  name: 'Green Tree Tavern',
  sub: 'Lake & West Water streets',
  distance: '0.2 mi',
  bearing: -80,
  grade: 'inferred',
  kind: 'Tavern · frame, two storeys',
  where: 'NE corner, Lake & West Water (now Canal) streets',
  lead: 'A frame tavern at the forks, kept by James Kinzie — the first such house of any pretension on the West Side.',
  facts: [{
    label: 'Built',
    value: '1833',
    grade: 'documented'
  }, {
    label: 'Storeys',
    value: 'Two',
    grade: 'documented'
  }, {
    label: 'Roof',
    value: 'Gable',
    grade: 'inferred'
  }, {
    label: 'Siding',
    value: 'Clapboard, unpainted',
    grade: 'conjectural'
  }]
}, {
  id: 'wolf',
  group: 'Taverns',
  name: 'Wolf Tavern',
  sub: 'Wolf Point',
  distance: '0.3 mi',
  bearing: 160,
  grade: 'conjectural',
  kind: 'Tavern · log',
  where: 'Wolf Point, at the confluence',
  lead: 'Log tavern on the point itself — the apex of the forks, and of our present disruption.',
  facts: [{
    label: 'Built',
    value: 'c. 1828',
    grade: 'inferred'
  }, {
    label: 'Walls',
    value: 'Hewn log',
    grade: 'inferred'
  }]
}, {
  id: 'bridge',
  group: 'Works',
  name: 'Dearborn Street drawbridge',
  sub: 'Main stem of the river',
  distance: '0.4 mi',
  bearing: 110,
  grade: 'documented',
  kind: 'Bridge · timber drawbridge',
  where: 'Dearborn Street, across the main stem',
  lead: 'A timber drawbridge of two leaves, notorious for its delays to the carriage trade.',
  facts: [{
    label: 'Built',
    value: '1834',
    grade: 'documented'
  }, {
    label: 'Span',
    value: '≈ 300 ft',
    grade: 'inferred'
  }]
}];
const KINDS = [['all', 'All', 4], ['Taverns', 'Taverns', 3], ['Works', 'Works', 1], ['Dwellings', 'Dwellings', 0]];
function Arrival({
  year,
  go
}) {
  const [q, setQ] = React.useState('');
  const [kind, setKind] = React.useState('all');
  const [conf, setConf] = React.useState(true);
  const [sel, setSel] = React.useState('greentree');
  const rows = STRUCTURES.filter(s => (kind === 'all' || s.group === kind) && s.name.toLowerCase().includes(q.toLowerCase()));
  const groups = [...new Set(rows.map(r => r.group))];
  const s = STRUCTURES.find(x => x.id === sel);
  return /*#__PURE__*/React.createElement("div", {
    className: "arrival"
  }, /*#__PURE__*/React.createElement("div", {
    className: "arrival-plate",
    style: {
      backgroundImage: 'url(' + ((window.ERAS.find(e => e.id === year) || {}).plate || '../../assets/imagery/wolf-point-1833.jpg') + ')',
      opacity: conf ? 1 : .85
    }
  }), /*#__PURE__*/React.createElement("div", {
    className: "arrival-scan"
  }), /*#__PURE__*/React.createElement("header", {
    className: "hud"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 22,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement(BrandMark, {
    code: year
  }), /*#__PURE__*/React.createElement("span", {
    className: "c4d-station"
  }, "Arrived ", year, ".07.01", /*#__PURE__*/React.createElement("i", null), "14:20 local")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 14,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement(ATelemetry, {
    items: [{
      label: 'Return window',
      value: '05:58:12'
    }, {
      label: 'Drift',
      value: '±0.4 d',
      state: 'warn'
    }]
  }), /*#__PURE__*/React.createElement(AButton, {
    variant: "secondary",
    size: "sm",
    onClick: () => go('home')
  }, "Recall"))), /*#__PURE__*/React.createElement("div", {
    className: "hud-body"
  }, /*#__PURE__*/React.createElement("aside", {
    className: "drawer"
  }, /*#__PURE__*/React.createElement(ASection, {
    title: "Register of structures",
    meta: "In view",
    metaValue: rows.length
  }), /*#__PURE__*/React.createElement(SearchField, {
    value: q,
    onChange: setQ,
    placeholder: "Search the 1835 register\u2026"
  }), /*#__PURE__*/React.createElement("div", {
    className: "pills"
  }, KINDS.map(([id, l, n]) => /*#__PURE__*/React.createElement(Pill, {
    key: id,
    pressed: kind === id,
    count: n,
    disabled: n === 0,
    onClick: () => setKind(id)
  }, l))), /*#__PURE__*/React.createElement(Toggle, {
    label: "Confidence view",
    checked: conf,
    onChange: setConf
  }), /*#__PURE__*/React.createElement("div", {
    className: "list"
  }, groups.map(g => /*#__PURE__*/React.createElement(React.Fragment, {
    key: g
  }, /*#__PURE__*/React.createElement(ResultGroup, {
    label: g,
    count: rows.filter(r => r.group === g).length
  }), rows.filter(r => r.group === g).map(r => /*#__PURE__*/React.createElement(ResultRow, _extends({
    key: r.id
  }, r, {
    grade: conf ? r.grade : undefined,
    active: sel === r.id,
    onClick: () => setSel(r.id)
  }))))), rows.length === 0 && /*#__PURE__*/React.createElement("p", {
    style: {
      padding: '18px 15px',
      color: 'var(--ink-dim)',
      margin: 0
    }
  }, "Nothing in the register by that name. Try \u201Ctavern\u201D, or ask the constable.")), conf && /*#__PURE__*/React.createElement("div", {
    className: "legend"
  }, /*#__PURE__*/React.createElement(ConfidenceGrade, {
    grade: "documented"
  }), /*#__PURE__*/React.createElement(ConfidenceGrade, {
    grade: "inferred"
  }), /*#__PURE__*/React.createElement(ConfidenceGrade, {
    grade: "conjectural"
  }))), s && /*#__PURE__*/React.createElement(BuildingCard, {
    key: s.id,
    title: s.name,
    kind: s.kind,
    where: /*#__PURE__*/React.createElement("strong", null, s.where),
    lead: s.lead,
    facts: conf ? s.facts : s.facts.map(f => ({
      ...f,
      grade: undefined
    })),
    flags: s.grade !== 'documented' ? [{
      text: 'Geometry partly reconstructed — see Evidence.'
    }] : [],
    tabs: [{
      id: 'ev',
      label: 'Evidence',
      count: s.facts.length,
      content: s.facts.length + ' attributes graded; ' + s.facts.filter(f => f.grade === 'documented').length + ' attested by a source.'
    }, {
      id: 'src',
      label: 'Sources',
      count: 2,
      content: 'Andreas, History of Chicago (1884), vol. I · Moses & Kirkland (1895).'
    }, {
      id: 'res',
      label: 'Residents',
      count: 1,
      content: 'Keeper recorded in the 1835 directory.'
    }],
    onClose: () => setSel(null)
  })));
}
window.Arrival = Arrival;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/observatory/Arrival.jsx", error: String((e && e.message) || e) }); }

// ui_kits/observatory/Briefing.jsx
try { (() => {
const {
  Masthead: BMasthead,
  MachineSelector: BMachineSelector,
  Chronometer: BChronometer,
  YearReadout,
  IndicatorLamp,
  TransitSequence,
  Placard,
  EngageButton,
  Telemetry: BTelemetry
} = window.Chicago4DTemporalObservatory_8fcc19;
function Briefing({
  skin,
  setSkin,
  year,
  go,
  engage
}) {
  const era = window.ERAS.find(e => e.id === year) || window.ERAS[0];
  return /*#__PURE__*/React.createElement("div", {
    className: "frame"
  }, /*#__PURE__*/React.createElement(BMasthead, {
    status: "Coordinate locked"
  }, /*#__PURE__*/React.createElement(BMachineSelector, {
    compact: true,
    value: skin,
    onChange: setSkin
  })), /*#__PURE__*/React.createElement("section", {
    className: "brief"
  }, /*#__PURE__*/React.createElement("div", {
    className: "instrument",
    style: {
      display: 'grid'
    }
  }, /*#__PURE__*/React.createElement(BChronometer, {
    size: 400,
    phase: "lock",
    note: 'Lock · ' + era.name
  })), /*#__PURE__*/React.createElement("div", {
    className: "brief-panel"
  }, /*#__PURE__*/React.createElement(TransitSequence, {
    current: 1
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 26,
      alignItems: 'flex-end',
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement(YearReadout, {
    year: era.year,
    size: 54
  }), /*#__PURE__*/React.createElement("div", {
    className: "lamps"
  }, /*#__PURE__*/React.createElement(IndicatorLamp, {
    label: "Time"
  }), /*#__PURE__*/React.createElement(IndicatorLamp, {
    label: "Map"
  }), /*#__PURE__*/React.createElement(IndicatorLamp, {
    label: "Archive",
    tone: "accent"
  }))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("p", {
    className: "eyebrow",
    style: {
      marginBottom: 8
    }
  }, era.index, " / ", era.name), /*#__PURE__*/React.createElement("h2", {
    style: {
      font: 'var(--display-weight) 38px/1.1 var(--font-display)',
      letterSpacing: 'var(--display-tracking)',
      margin: '0 0 10px'
    }
  }, era.title), /*#__PURE__*/React.createElement("p", {
    className: "coord"
  }, "41.8880\xB0 N \xB7 87.6380\xB0 W \xB7 ", era.footLeft), /*#__PURE__*/React.createElement("p", {
    className: "lede",
    style: {
      margin: '12px 0 0',
      lineHeight: 1.7
    }
  }, "Coordinate locked on the forks. Interval drift within tolerance. Passengers are reminded that ", era.year, " has no electric light to speak of, no sewer, and strong opinions on hats.")), /*#__PURE__*/React.createElement(BTelemetry, {
    items: [{
      label: 'Field',
      value: '0.998',
      state: 'ok'
    }, {
      label: 'Charge',
      value: '94%'
    }, {
      label: 'Return window',
      value: '06:00:00'
    }]
  }), /*#__PURE__*/React.createElement("div", {
    className: "actions"
  }, /*#__PURE__*/React.createElement(EngageButton, {
    size: "lg",
    onClick: engage
  }, "Engage ", era.year), /*#__PURE__*/React.createElement(EngageButton, {
    variant: "ghost",
    onClick: () => go('home')
  }, "\u2190 Return to coordinates")), /*#__PURE__*/React.createElement(Placard, {
    title: "Stand clear of the aperture",
    note: "Circle-3 clearance \xB7 kindly keep hands and parasols inside the field"
  }))));
}
window.Briefing = Briefing;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/observatory/Briefing.jsx", error: String((e && e.message) || e) }); }

// ui_kits/observatory/Home.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const {
  Masthead,
  MachineSelector,
  Chronometer,
  AcquisitionStatus,
  Telemetry,
  SectionLine,
  EraCard
} = window.Chicago4DTemporalObservatory_8fcc19;
const ERAS = [{
  id: '1835',
  index: '01',
  name: 'River settlement',
  year: '1835',
  title: 'At the river’s forks',
  body: 'Timber roofs, a drawbridge on Dearborn, and a town not yet a city. Mud to the axle.',
  imageSrc: '../../assets/imagery/wolf-point-1833.jpg',
  plate: '../../assets/imagery/wolf-point-1833.jpg',
  footLeft: '1835.07.01 · Drift ±0.4 d',
  primary: true
}, {
  id: '1904',
  index: '02',
  name: 'Prairie Avenue',
  year: '1904',
  title: 'The city in stone',
  body: 'Glessner House and the carriage trade, lit by gas and the newfangled electric.',
  imageSrc: '../../assets/imagery/prairie-avenue-street.png',
  plate: '../../assets/imagery/prairie-avenue-glass-plate.png',
  footLeft: '1904.07.01 · Drift ±0.1 d'
}, {
  id: '1812',
  index: '03',
  name: 'Fort Dearborn',
  year: '1812',
  title: 'Where river meets lake',
  body: 'Signature acquired; the scene is still under survey. Not yet fit for passengers.',
  imageSrc: '../../assets/imagery/fort-dearborn-1812.jpg',
  pending: true,
  state: 'Calibrating',
  footLeft: 'Survey in progress',
  footRight: 'Status'
}];
const STAGES = ['Sweeping the interval…', '1835 · signature resolved at the forks', '1904 · Prairie Avenue resolved', 'Three coordinates resolved. Field nominal.'];
function Home({
  skin,
  setSkin,
  go
}) {
  const [stage, setStage] = React.useState(0);
  React.useEffect(() => {
    const ts = [1, 2, 3].map(i => setTimeout(() => setStage(i), 500 + i * 450));
    return () => ts.forEach(clearTimeout);
  }, []);
  return /*#__PURE__*/React.createElement("div", {
    className: "frame"
  }, /*#__PURE__*/React.createElement(Masthead, {
    status: stage < 3 ? 'Acquiring' : 'Field nominal'
  }, /*#__PURE__*/React.createElement(MachineSelector, {
    compact: true,
    value: skin,
    onChange: setSkin
  })), /*#__PURE__*/React.createElement("section", {
    className: "intro"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("p", {
    className: "eyebrow"
  }, "41\xB0 53\u2032 N \xA0 87\xB0 38\u2032 W \xA0/\xA0 Wolf Point confluence \xA0/\xA0 Clearance Circle-3"), /*#__PURE__*/React.createElement("h1", {
    className: "hero"
  }, "Wolf Point aperture:", /*#__PURE__*/React.createElement("br", null), /*#__PURE__*/React.createElement("em", null, "open.")), /*#__PURE__*/React.createElement("p", {
    className: "lede"
  }, "In 1965 a criticality excursion beneath the Circle campus tore a standing aperture at the apex of the river\u2019s forks. The Confluence Laboratory has resolved three coordinates in the interval. Select one; the Apparatus will see to the rest."), /*#__PURE__*/React.createElement(AcquisitionStatus, {
    busy: stage < 3,
    message: STAGES[stage],
    count: '0' + stage + ' / 03'
  })), /*#__PURE__*/React.createElement("div", {
    className: "instrument"
  }, /*#__PURE__*/React.createElement(Chronometer, {
    size: 400,
    phase: stage < 3 ? 'scan' : 'lock'
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginBottom: 30
    }
  }, /*#__PURE__*/React.createElement(Telemetry, {
    items: [{
      label: 'Reactor',
      value: '87.2%'
    }, {
      label: 'Field coherence',
      value: '0.998',
      state: 'ok'
    }, {
      label: 'Interval drift',
      value: '±0.4 d',
      state: 'warn'
    }, {
      label: 'Dosimetry',
      value: 'Nominal',
      state: 'ok'
    }, {
      label: 'Passengers',
      value: '01'
    }]
  })), /*#__PURE__*/React.createElement(SectionLine, {
    title: "Resolved coordinates",
    meta: "Locked 02 \xB7 Calibrating",
    metaValue: "01"
  }), /*#__PURE__*/React.createElement("div", {
    className: "era-grid"
  }, ERAS.map((e, i) => /*#__PURE__*/React.createElement(EraCard, _extends({
    key: e.id
  }, e, {
    state: e.state || (stage > (e.id === '1835' ? 0 : 1) ? 'Coordinate locked' : 'Resolving…'),
    onClick: () => go(e.pending ? 'pending' : 'brief', e.id)
  })))), /*#__PURE__*/React.createElement("footer", {
    className: "foot"
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0
    }
  }, "A researched reconstruction. Every surface carries its evidence."), /*#__PURE__*/React.createElement("span", {
    className: "c4d-label"
  }, "Confluence Laboratory \xB7 Univ. of Illinois, Chicago Circle \xB7 Est. 1965")));
}
window.Home = Home;
window.ERAS = ERAS;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/observatory/Home.jsx", error: String((e && e.message) || e) }); }

// ui_kits/observatory/Pending.jsx
try { (() => {
const {
  Masthead: PMasthead,
  MachineSelector: PMachineSelector,
  Chronometer: PChronometer,
  AcquisitionStatus: PAcq,
  EngageButton: PButton,
  SectionLine: PSection
} = window.Chicago4DTemporalObservatory_8fcc19;
function Pending({
  skin,
  setSkin,
  go
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "frame"
  }, /*#__PURE__*/React.createElement(PMasthead, {
    status: "Calibrating"
  }, /*#__PURE__*/React.createElement(PMachineSelector, {
    compact: true,
    value: skin,
    onChange: setSkin
  })), /*#__PURE__*/React.createElement("section", {
    className: "pending"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("p", {
    className: "eyebrow"
  }, "Temporal signature / 1812 / Fort Dearborn"), /*#__PURE__*/React.createElement("h1", {
    className: "hero"
  }, "Before", /*#__PURE__*/React.createElement("br", null), /*#__PURE__*/React.createElement("em", null, "the city.")), /*#__PURE__*/React.createElement("p", {
    className: "lede"
  }, "The 1812 signature is resolved, but the landscape is not yet surveyed to passenger standard. The Laboratory declines to send anyone to a place it can only guess at \u2014 a dashed poor show for a traveller, and worse for the record."), /*#__PURE__*/React.createElement(PAcq, {
    busy: true,
    message: "Survey in progress \xB7 reconstruction pending",
    count: ""
  })), /*#__PURE__*/React.createElement("div", {
    className: "instrument"
  }, /*#__PURE__*/React.createElement(PChronometer, {
    size: 360,
    phase: "scan",
    note: "Calibrating \xB7 1812"
  }))), /*#__PURE__*/React.createElement(PSection, {
    title: "Meanwhile"
  }, /*#__PURE__*/React.createElement("div", {
    className: "actions"
  }, /*#__PURE__*/React.createElement(PButton, {
    variant: "ghost",
    onClick: () => go('home')
  }, "\u2190 All coordinates"), /*#__PURE__*/React.createElement(PButton, {
    variant: "secondary",
    arrow: true,
    onClick: () => go('brief', '1835')
  }, "Lock 1835"))));
}
window.Pending = Pending;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/observatory/Pending.jsx", error: String((e && e.message) || e) }); }

__ds_ns.BrandMark = __ds_scope.BrandMark;

__ds_ns.Masthead = __ds_scope.Masthead;

__ds_ns.EngageButton = __ds_scope.EngageButton;

__ds_ns.MACHINES = __ds_scope.MACHINES;

__ds_ns.MachineSelector = __ds_scope.MachineSelector;

__ds_ns.Pill = __ds_scope.Pill;

__ds_ns.SearchField = __ds_scope.SearchField;

__ds_ns.Tabs = __ds_scope.Tabs;

__ds_ns.Toggle = __ds_scope.Toggle;

__ds_ns.EraArt = __ds_scope.EraArt;

__ds_ns.EraCard = __ds_scope.EraCard;

__ds_ns.SectionLine = __ds_scope.SectionLine;

__ds_ns.AcquisitionStatus = __ds_scope.AcquisitionStatus;

__ds_ns.Chronometer = __ds_scope.Chronometer;

__ds_ns.IndicatorLamp = __ds_scope.IndicatorLamp;

__ds_ns.Placard = __ds_scope.Placard;

__ds_ns.Telemetry = __ds_scope.Telemetry;

__ds_ns.TransitSequence = __ds_scope.TransitSequence;

__ds_ns.YearReadout = __ds_scope.YearReadout;

__ds_ns.DepartureOverlay = __ds_scope.DepartureOverlay;

__ds_ns.BuildingCard = __ds_scope.BuildingCard;

__ds_ns.ConfidenceGrade = __ds_scope.ConfidenceGrade;

__ds_ns.ResultRow = __ds_scope.ResultRow;

__ds_ns.ResultGroup = __ds_scope.ResultGroup;

})();
