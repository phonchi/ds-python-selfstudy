const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
function grab(name) {
  const i = src.indexOf(`const ${name} = [`);
  if (i < 0) return null;
  const start = src.indexOf('[', i);
  let depth = 0, j = start, inStr = null;
  for (; j < src.length; j++) {
    const c = src[j];
    if (inStr) {
      if (c === '\\') { j++; continue; }
      if (c === inStr) inStr = null;
      continue;
    }
    if (c === "'" || c === '"' || c === '`') { inStr = c; continue; }
    if (c === '[') depth++;
    else if (c === ']') { depth--; if (depth === 0) { j++; break; } }
  }
  return eval(src.slice(start, j));
}
console.log(JSON.stringify({quiz: grab('QUIZ_DATA'), cards: grab('CARD_DATA')}, null, 1));
