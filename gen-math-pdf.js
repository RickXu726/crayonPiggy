const PDFDocument = require('pdfkit');
const fs = require('fs');

// 固定种子，保证每天题目不同但可重现
const seed = new Date().getDate() * 1000000 + new Date().getMonth() * 10000 + new Date().getFullYear();
let randomState = seed;
function random() {
    randomState = (randomState * 9301 + 49297) % 233280;
    return randomState / 233280;
}

function genAddSub() {
    if (random() > 0.5) {
        const a = Math.floor(random() * 21);
        const b = Math.floor(random() * (21 - a));
        return `${a} + ${b} = ______`;
    } else {
        const a = Math.floor(random() * 21);
        const b = Math.floor(random() * (a + 1));
        return `${a} - ${b} = ______`;
    }
}

function genChain() {
    const type = Math.floor(random() * 3);
    if (type === 0) {
        let a = Math.floor(random() * 10) + 1;
        let b = Math.floor(random() * 10) + 1;
        let c = Math.max(1, 20 - a - b);
        return `${a} + ${b} + ${c} = ______`;
    } else if (type === 1) {
        const a = Math.floor(random() * 10) + 10;
        const b = Math.floor(random() * 5) + 1;
        const c = Math.floor(random() * 5) + 1;
        return `${a} - ${b} - ${c} = ______`;
    } else {
        let a = Math.floor(random() * 10) + 5;
        let b = Math.floor(random() * 5) + 1;
        let c = Math.floor(random() * 10) + 1;
        while (a - b + c > 20 || a - b + c < 0) { a = Math.floor(random() * 10) + 5; b = Math.floor(random() * 5) + 1; }
        return `${a} - ${b} + ${c} = ______`;
    }
}

function genCompare() {
    const e1 = genAddSub().replace(' = ______', '');
    const e2 = genAddSub().replace(' = ______', '');
    // 使用 < > = 符号代替 ○
    return `${e1}  ?  ${e2}`;
}

const part1 = Array.from({length: 50}, genAddSub);
const part2 = Array.from({length: 20}, genChain);
const part3 = Array.from({length: 10}, genCompare);

const doc = new PDFDocument({ size: 'A4', margins: { top: 40, bottom: 40, left: 40, right: 40 } });
const outputPath = "/home/admin/.openclaw/workspace/Mabel's math/2026-03-23 算数.pdf";

doc.pipe(fs.createWriteStream(outputPath));

// 标题
doc.fontSize(20).font('Helvetica-Bold').text('2026-03-23 Suan Shu', { align: 'center' });
doc.moveDown(0.3);
doc.fontSize(12).font('Helvetica').text('Name: __________    Date: __________    Score: __________', { align: 'center' });
doc.moveDown(0.5);

// 第一部分：50 道题，5 列 x 10 行
doc.fontSize(11).font('Helvetica-Bold').text('Part 1: Addition/Subtraction (50)', { align: 'left' });
doc.moveDown(0.3);

const colWidth = 110;
const rowHeight = 18;
const startX = 40;
let y = doc.y;

doc.fontSize(9).font('Helvetica');
for (let row = 0; row < 10; row++) {
    for (let col = 0; col < 5; col++) {
        const idx = row * 5 + col;
        const x = startX + col * colWidth;
        doc.text(`${idx+1}. ${part1[idx]}`, x, y, { width: colWidth - 5, height: rowHeight });
    }
    y += rowHeight;
}

doc.moveDown(0.5);

// 第二部分：20 道题，4 列 x 5 行
doc.fontSize(11).font('Helvetica-Bold').text('Part 2: Chain Operations (20)', { align: 'left' });
doc.moveDown(0.3);

y = doc.y;
doc.fontSize(9).font('Helvetica');
for (let row = 0; row < 5; row++) {
    for (let col = 0; col < 4; col++) {
        const idx = row * 4 + col;
        const x = startX + col * 130;
        doc.text(`${idx+1}. ${part2[idx]}`, x, y, { width: 125, height: rowHeight });
    }
    y += rowHeight;
}

doc.moveDown(0.5);

// 第三部分：10 道题，2 列 x 5 行
doc.fontSize(11).font('Helvetica-Bold').text('Part 3: Compare (10) - Fill in >, <, or =', { align: 'left' });
doc.moveDown(0.3);

y = doc.y;
doc.fontSize(10).font('Helvetica');
for (let row = 0; row < 5; row++) {
    for (let col = 0; col < 2; col++) {
        const idx = row * 2 + col;
        const x = startX + col * 250;
        doc.text(`${idx+1}. ${part3[idx]}`, x, y, { width: 240, height: rowHeight + 2 });
    }
    y += rowHeight + 2;
}

// 页脚
doc.moveDown(1);
doc.fontSize(10).font('Helvetica').text('Parent Signature: __________    Time: __________ min', { align: 'center' });

doc.end();

console.log('PDF generated:', outputPath);
