(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
// Generated by LiveScript 1.3.0
(function(){
  var ret;
  ret = {
    id: 'spinner',
    type: 'spinner',
    name: 'Spinner',
    desc: "Most common and popular loader.",
    tags: ['spinner', 'preloader', 'ajax', 'loading', 'icon'],
    slug: "ajax-spinner-preloader",
    license: 'free',
    edit: {
      color: {
        name: "Color",
        type: 'color',
        'default': '#fe718d',
        priority: 1.1
      },
      colorful: {
        name: "Multi color",
        type: 'boolean',
        'default': false,
        priority: 1.2
      },
      round: {
        name: "Corner",
        type: 'number',
        'default': 50,
        min: 0,
        max: 100,
        priority: 1.3
      },
      w: {
        name: "Bar Width",
        type: 'number',
        'default': 6,
        min: 1,
        max: 100
      },
      h: {
        name: "Bar Height",
        type: 'number',
        'default': 12,
        min: 1,
        max: 100
      },
      count: {
        name: "Bar Count",
        type: 'number',
        'default': 12,
        min: 2,
        max: 100
      },
      radius: {
        name: "Radius",
        type: 'number',
        'default': 20,
        min: 0,
        max: 50
      },
      palette: {
        'default': {
          colors: ['#fe718d', '#f47e60', '#f8b26a', '#abbd81', '#849b87', '#6492ac', '#637cb5', '#6a63b6']
        }
      }
    },
    download: function(arg$){
      var type, ref$, cfg, lc, s, count, html, max, rx, ref1$, ry, css, pal, i$, i, angle, b, c;
      type = arg$.type;
      if (type !== 'css') {
        return;
      }
      ref$ = [this.config, this.local], cfg = ref$[0], lc = ref$[1];
      s = (ref$ = cfg.size / 100) > 1 ? ref$ : 1;
      count = cfg.count;
      html = repeatString$("<div></div>", count);
      max = Math.max(cfg.w, cfg.h);
      rx = (ref$ = max * cfg.round * 0.01) < (ref1$ = cfg.w / 2) ? ref$ : ref1$;
      ry = (ref$ = max * cfg.round * 0.01) < (ref1$ = cfg.h / 2) ? ref$ : ref1$;
      css = "@keyframes $id {\n  0% { opacity: 1 }\n  100% { opacity: 0 }\n}\n.$id div {\n  left: " + s * (50 - cfg.w / 2) + "px;\n  top: " + s * (50 - cfg.radius - cfg.h / 2) + "px;\n  position: absolute;\n  animation: $id linear " + 1 / cfg.speed + "s infinite;\n  background: " + cfg.color + ";\n  width: " + cfg.w * s + "px;\n  height: " + cfg.h * s + "px;\n  border-radius: " + rx * s + "px / " + ry * s + "px;\n  transform-origin: " + s * cfg.w / 2 + "px " + s * (cfg.h / 2 + cfg.radius) + "px;\n}";
      pal = cfg.palette.colors.map(function(it){
        return ldColor.web(it);
      });
      for (i$ = 0; i$ < count; ++i$) {
        i = i$;
        angle = 360 * i / count;
        b = -(count - i - 1) / (count * cfg.speed);
        c = cfg.colorful
          ? pal[i % pal.length]
          : cfg.color;
        css += ".$id div:nth-child(" + (i + 1) + ") {\n  transform: rotate(" + angle + "deg);\n  animation-delay: " + b + "s;\n  background: " + c + ";\n}";
      }
      return {
        html: html,
        css: css
      };
    },
    dom: function(cfg){
      var svg, count, w, h, c, r, pal, vs, ts, max, rx, ref$, ref1$, ry, i$, i, x, y, a, b;
      svg = [];
      count = cfg.count;
      w = cfg.w;
      h = cfg.h;
      c = cfg.color;
      r = cfg.round;
      pal = cfg.palette.colors.map(function(it){
        return ldColor.web(it);
      });
      vs = "1;0";
      ts = "0;1";
      max = Math.max(w, h);
      rx = (ref$ = max * r * 0.01) < (ref1$ = w / 2) ? ref$ : ref1$;
      ry = (ref$ = max * r * 0.01) < (ref1$ = h / 2) ? ref$ : ref1$;
      for (i$ = 0; i$ < count; ++i$) {
        i = i$;
        x = 50 - +cfg.w / 2;
        y = 50 - +cfg.h / 2 - +cfg.radius;
        a = 360 * i / count;
        b = -1 * (count - i - 1) / (count * cfg.speed);
        if (cfg.colorful) {
          c = pal[i % pal.length];
        }
        svg.push("<g transform=\"rotate(" + a + " 50 50)\">\n  <rect x=\"" + x + "\" y=\"" + y + "\" rx=\"" + rx + "\" ry=\"" + ry + "\" width=\"" + w + "\" height=\"" + h + "\" fill=\"" + c + "\">\n    <animate attributeName=\"opacity\" values=\"" + vs + "\" keyTimes=\"" + ts + "\" dur=\"" + 1 / cfg.speed + "s\"\n    begin=\"" + b + "s\" repeatCount=\"indefinite\"/>\n  </rect>\n</g>");
      }
      return svg.join("");
    }
  };
  if (typeof module != 'undefined' && module !== null) {
    module.exports = ret;
  }
  if (typeof ModManager != 'undefined' && ModManager !== null) {
    ModManager.register(ret);
  }
  return ret;
})();
function repeatString$(str, n){
  for (var r = ''; n > 0; (n >>= 1) && (str += str)) if (n & 1) r += str;
  return r;
}
},{}]},{},[1]);
