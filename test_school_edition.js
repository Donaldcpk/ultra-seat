/**
 * 終極課室座位表 — 核心邏輯單測（班主任課室場景）
 * 執行：node test_school_edition.js
 */

function checkAdjacency(row1, col1, row2, col2, constraintType) {
    const rowDiff = Math.abs(row1 - row2);
    const colDiff = Math.abs(col1 - col2);
    switch (constraintType) {
        case 'all':
            return rowDiff <= 1 && colDiff <= 1 && !(rowDiff === 0 && colDiff === 0);
        case 'horizontal':
            return rowDiff === 0 && colDiff === 1;
        case 'vertical':
            return rowDiff === 1 && colDiff === 0;
        default:
            return false;
    }
}

function maxCheckerboardCapacity(availableSeats) {
    let black = 0, white = 0;
    for (const [r, c] of availableSeats) {
        if ((r + c) % 2 === 0) black++;
        else white++;
    }
    return Math.max(black, white);
}

function pickCheckerboardColorSeats(availableSeats, needCount) {
    const black = availableSeats.filter(([r, c]) => (r + c) % 2 === 0);
    const white = availableSeats.filter(([r, c]) => (r + c) % 2 === 1);
    const candidates = [];
    if (black.length >= needCount) candidates.push(black);
    if (white.length >= needCount) candidates.push(white);
    if (candidates.length === 0) return null;
    candidates.sort((a, b) => b.length - a.length);
    return candidates[0];
}

function orthogonalNeighbors(row, col, rows, cols) {
    return [
        [row - 1, col], [row + 1, col], [row, col - 1], [row, col + 1]
    ].filter(([r, c]) => r >= 0 && r < rows && c >= 0 && c < cols);
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function countMovedStudents(assignmentPairs, previousMap) {
    if (!previousMap || previousMap.size === 0) return { moved: 0, comparable: 0 };
    let moved = 0;
    let comparable = 0;
    assignmentPairs.forEach(([student, seat]) => {
        if (!previousMap.has(student.id)) return;
        comparable++;
        const prev = previousMap.get(student.id);
        if (prev[0] !== seat[0] || prev[1] !== seat[1]) moved++;
    });
    return { moved, comparable };
}

function solveCSP({ students, rows, cols, blocked, constraints, opts, previousMap, nodeLimit = 100000, timeMs = 5000 }) {
    let availableSeats = [];
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (!blocked.has(`${r}-${c}`)) availableSeats.push([r, c]);
        }
    }
    if (opts.checkerboard) {
        const colored = pickCheckerboardColorSeats(availableSeats, students.length);
        if (!colored) return { ok: false, nodes: 0 };
        availableSeats = colored;
    }
    const seats = availableSeats.map(s => [...s]);
    const assignment = new Map();
    const occupied = new Map();
    const start = Date.now();
    let nodes = 0;
    let timedOut = false;
    const hasPrevious = previousMap && previousMap.size > 0;
    const frontRowLimit = Math.min(2, rows);

    function isValid(student, seat, forbidPrevious) {
        const [row, col] = seat;
        const key = `${row}-${col}`;
        if (occupied.has(key)) return false;
        if (forbidPrevious && hasPrevious && previousMap.has(student.id)) {
            const prev = previousMap.get(student.id);
            if (prev[0] === row && prev[1] === col) return false;
        }
        if (opts.checkerboard) {
            for (const [nr, nc] of orthogonalNeighbors(row, col, rows, cols)) {
                const nk = `${nr}-${nc}`;
                if (blocked.has(nk)) continue;
                if (occupied.has(nk)) return false;
            }
        }
        if (opts.disperseGroup && student.classGroup) {
            for (const [nr, nc] of orthogonalNeighbors(row, col, rows, cols)) {
                const other = occupied.get(`${nr}-${nc}`);
                if (other && other.classGroup === student.classGroup) return false;
            }
        }
        for (const constraint of constraints) {
            if (constraint.student1 !== student.id && constraint.student2 !== student.id) continue;
            const otherId = constraint.student1 === student.id ? constraint.student2 : constraint.student1;
            const otherSeat = assignment.get(otherId);
            if (!otherSeat) continue;
            if (checkAdjacency(row, col, otherSeat[0], otherSeat[1], constraint.type)) return false;
        }
        return true;
    }

    function domainFor(student, forbidPrevious) {
        let domain = seats.filter(s => isValid(student, s, forbidPrevious));
        if (student.needsFront) {
            const front = domain.filter(([r]) => r < frontRowLimit);
            const back = domain.filter(([r]) => r >= frontRowLimit);
            domain = front.length ? front.concat(back) : domain;
        }
        if (hasPrevious && previousMap.has(student.id)) {
            const prev = previousMap.get(student.id);
            const pk = `${prev[0]}-${prev[1]}`;
            const moved = domain.filter(([r, c]) => `${r}-${c}` !== pk);
            const same = domain.filter(([r, c]) => `${r}-${c}` === pk);
            domain = moved.concat(same);
        }
        return domain;
    }

    function selectNext(remaining, forbidPrevious) {
        let best = null, bestCount = Infinity;
        for (const s of remaining) {
            const d = domainFor(s, forbidPrevious);
            if (d.length < bestCount) {
                bestCount = d.length;
                best = { student: s, domain: d };
                if (bestCount === 0) break;
            }
        }
        return best;
    }

    function bt(remaining, forbidPrevious) {
        nodes++;
        if (nodes > nodeLimit || Date.now() - start > timeMs) {
            timedOut = true;
            return false;
        }
        if (remaining.length === 0) return true;
        const pick = selectNext(remaining, forbidPrevious);
        if (!pick || pick.domain.length === 0) return false;
        const next = remaining.filter(s => s.id !== pick.student.id);
        for (const seat of pick.domain) {
            const key = `${seat[0]}-${seat[1]}`;
            assignment.set(pick.student.id, seat);
            occupied.set(key, pick.student);
            if (bt(next, forbidPrevious)) return true;
            assignment.delete(pick.student.id);
            occupied.delete(key);
            if (timedOut) return false;
        }
        return false;
    }

    function runSearch(forbidPrevious, restarts) {
        let best = null;
        let bestMoved = -1;
        for (let restart = 0; restart < restarts; restart++) {
            if (timedOut || nodes > nodeLimit) break;
            assignment.clear();
            occupied.clear();
            shuffleArray(seats);
            const remaining = shuffleArray([...students]);
            if (bt(remaining, forbidPrevious)) {
                const pairs = students.map(s => [s, assignment.get(s.id)]);
                const { moved, comparable } = countMovedStudents(pairs, previousMap);
                if (moved > bestMoved) {
                    bestMoved = moved;
                    best = { ok: true, assignment: pairs, nodes, moved, comparable };
                    if (comparable > 0 && moved === comparable) break;
                }
            }
        }
        return best;
    }

    let result = null;
    if (hasPrevious) result = runSearch(true, 4);
    if (!result) result = runSearch(false, 6);
    return result || { ok: false, nodes, timedOut };
}

function classifyConstraintReport({ students, constraints, rows }) {
    const frontLimit = Math.min(2, rows);
    const pairs = constraints.map(c => {
        const s1 = students.find(s => s.id === c.student1);
        const s2 = students.find(s => s.id === c.student2);
        let status = '未分配';
        if (s1 && s2 && s1.row != null && s2.row != null) {
            status = checkAdjacency(s1.row, s1.col, s2.row, s2.col, c.type) ? '失敗' : '已遵守';
        }
        return { student1: c.student1, student2: c.student2, status };
    });
    const frontIssues = students
        .filter(s => s.needsFront && s.row != null && s.row >= frontLimit)
        .map(s => s.id);
    return { pairs, frontIssues };
}

function buildAnalysisCsvRows({ rows, cols, seats, blocked, studentsById }) {
    const header = ['座位行', '座位列', '狀態', '班別', '學號', '姓名', '職務', '是否前排', '左鄰', '右鄰'];
    const out = [header];
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const key = `${r}-${c}`;
            let status = '空位';
            let classGroup = '', id = '', name = '', position = '', frontFlag = '';
            if (blocked.has(key)) status = '阻擋';
            else if (seats[r][c]) {
                const s = seats[r][c];
                status = '已分配';
                classGroup = s.classGroup || '';
                id = s.id;
                name = s.name;
                position = s.position || '';
                frontFlag = s.needsFront ? '是' : '否';
            }
            const left = c > 0 ? seats[r][c - 1] : null;
            const right = c < cols - 1 ? seats[r][c + 1] : null;
            out.push([
                String(r + 1), String(c + 1), status, classGroup, id, name, position, frontFlag,
                left ? left.name : '', right ? right.name : ''
            ]);
        }
    }
    return out;
}

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function formatSchoolFormTitle(className, room) {
    const cls = String(className || '').trim() || '　';
    const rm = String(room || '').trim() || '　';
    return `${cls}班/科座位表 (${rm}室)`;
}

function schoolFormGridColumns(cols) {
    const n = Number(cols);
    if (n >= 2 && n % 2 === 0) {
        const half = n / 2;
        return `repeat(${half}, 1fr) 18px repeat(${half}, 1fr)`;
    }
    return `repeat(${n}, 1fr)`;
}

function buildSchoolFormHtml(opts) {
    const className = opts.className || '';
    const room = opts.room || '';
    const rows = opts.rows;
    const cols = opts.cols;
    const seats = opts.seats || [];
    const blocked = opts.blockedSeats instanceof Set
        ? opts.blockedSeats
        : new Set(opts.blockedSeats || []);
    const teachers = opts.teachers || ['', '', ''];
    const selected = opts.selectedSeat || null;
    const interactive = !!opts.interactive;

    const title = formatSchoolFormTitle(className, room);
    const hasAisle = cols % 2 === 0;
    const half = cols / 2;
    const colStyle = schoolFormGridColumns(cols);

    let cells = '';
    for (let r = rows - 1; r >= 0; r--) {
        for (let c = 0; c < cols; c++) {
            if (hasAisle && c === half) {
                cells += '<div class="school-aisle" aria-hidden="true"></div>';
            }
            const key = `${r}-${c}`;
            const student = seats[r] && seats[r][c] ? seats[r][c] : null;
            const isBlocked = blocked.has(key);
            const isSelected = selected && selected[0] === r && selected[1] === c;
            let cls = 'seat';
            if (isBlocked) cls += ' blocked';
            else if (student) {
                cls += ' occupied';
                if (student.needsFront) cls += ' front-pref';
            }
            if (isSelected) cls += ' selected';

            let inner = '';
            if (isBlocked) inner = '擋';
            else if (student) inner = `<strong>${escapeHtml(student.name || '')}</strong>`;

            const click = interactive ? ` onclick="onSeatClick(${r},${c})"` : '';
            cells += `<div class="${cls}" data-row="${r}" data-col="${c}"${click}>${inner}</div>`;
        }
    }

    const t1 = escapeHtml(teachers[0] || '');
    const t2 = escapeHtml(teachers[1] || '');
    const t3 = escapeHtml(teachers[2] || '');

    return `<div class="school-form">
        <div class="school-form-title">${escapeHtml(title)}</div>
        <div class="school-form-grid" style="grid-template-columns:${colStyle}">${cells}</div>
        <div class="school-form-front-bar"></div>
        <div class="school-form-footer">
            <div class="school-form-teachers">
                <div>Class Teacher 1${t1 ? '：' + t1 : ''}</div>
                <div>Class Teacher 2${t2 ? '：' + t2 : ''}</div>
                <div>Class Teacher 3${t3 ? '：' + t3 : ''}</div>
            </div>
            <div class="school-form-desk">教師桌</div>
        </div>
    </div>${interactive ? '<p class="school-form-hint no-print">下方為課室前方（教師桌）。偶數欄會在中間留走道。</p>' : ''}`;
}

function assert(cond, msg) {
    if (!cond) throw new Error('FAIL: ' + msg);
}

let passed = 0;

// 1) 相鄰判定
assert(checkAdjacency(0, 0, 0, 1, 'horizontal'), 'horizontal neighbor');
assert(!checkAdjacency(0, 0, 1, 0, 'horizontal'), 'not horizontal');
passed++;

// 2) 典型課室：40 人、6×7、3 組不可同坐
{
    const students = [];
    for (let i = 0; i < 40; i++) {
        students.push({ id: String(i + 1).padStart(2, '0'), classGroup: '中三甲', needsFront: i === 3 });
    }
    const constraints = [
        { student1: '05', student2: '07', type: 'all' },
        { student1: '11', student2: '13', type: 'horizontal' },
        { student1: '22', student2: '24', type: 'vertical' }
    ];
    const blocked = new Set(['5-6', '5-5']);
    const result = solveCSP({
        students, rows: 6, cols: 7, blocked, constraints,
        opts: { checkerboard: false, disperseGroup: false }
    });
    assert(result.ok, '40 students 6x7 with 3 keep-apart should solve');
    const a = result.assignment.find(([s]) => s.id === '05')[1];
    const b = result.assignment.find(([s]) => s.id === '07')[1];
    assert(!checkAdjacency(a[0], a[1], b[0], b[1], 'all'), '05 and 07 not adjacent');
    passed++;
}

// 3) 週更：有上次座位時應盡量換位
{
    const students = [];
    for (let i = 0; i < 12; i++) students.push({ id: 'S' + i, needsFront: false });
    const first = solveCSP({
        students, rows: 3, cols: 4, blocked: new Set(), constraints: [],
        opts: { checkerboard: false, disperseGroup: false }
    });
    assert(first.ok, 'first assign');
    const previousMap = new Map();
    first.assignment.forEach(([s, seat]) => previousMap.set(s.id, seat));

    const second = solveCSP({
        students, rows: 3, cols: 4, blocked: new Set(), constraints: [],
        opts: { checkerboard: false, disperseGroup: false },
        previousMap
    });
    assert(second.ok, 'rotation assign');
    assert(second.comparable === 12, 'all comparable');
    assert(second.moved === 12, 'all students should move when unconstrained derangement exists');
    // verify none stayed
    second.assignment.forEach(([s, seat]) => {
        const prev = previousMap.get(s.id);
        assert(prev[0] !== seat[0] || prev[1] !== seat[1], 'student moved ' + s.id);
    });
    passed++;
}

// 4) 無上次方案時 moved/comparable 為 0
{
    const students = [{ id: 'A' }, { id: 'B' }, { id: 'C' }];
    const result = solveCSP({
        students, rows: 2, cols: 2, blocked: new Set(), constraints: [],
        opts: { checkerboard: false, disperseGroup: false }
    });
    assert(result.ok, 'no previous');
    assert(result.moved === 0 && result.comparable === 0, 'no rotation stats');
    passed++;
}

// 5) 分析 CSV 欄位與左鄰右鄰
{
    const seats = [
        [
            { id: '01', name: '甲', classGroup: '中三甲', position: '', needsFront: true },
            { id: '02', name: '乙', classGroup: '中三甲', position: '', needsFront: false },
            null
        ],
        [null, null, null]
    ];
    const blocked = new Set(['1-2']);
    const rows = buildAnalysisCsvRows({
        rows: 2, cols: 3, seats, blocked, studentsById: {}
    });
    assert(rows[0].join(',') === '座位行,座位列,狀態,班別,學號,姓名,職務,是否前排,左鄰,右鄰', 'csv header');
    assert(rows.length === 1 + 2 * 3, 'all cells included');
    const r1c1 = rows.find(r => r[0] === '1' && r[1] === '1');
    assert(r1c1[2] === '已分配' && r1c1[7] === '是' && r1c1[8] === '' && r1c1[9] === '乙', 'front and right neighbor');
    const r1c2 = rows.find(r => r[0] === '1' && r[1] === '2');
    assert(r1c2[8] === '甲' && r1c2[9] === '', 'left neighbor of 乙');
    const blockedCell = rows.find(r => r[0] === '2' && r[1] === '3');
    assert(blockedCell[2] === '阻擋', 'blocked status');
    passed++;
}

// 6) 限制報告分類
{
    const students = [
        { id: '05', name: '張', row: 0, col: 0, needsFront: false },
        { id: '07', name: '吳', row: 0, col: 2, needsFront: false },
        { id: '04', name: '黃', row: 3, col: 1, needsFront: true }
    ];
    const constraints = [
        { student1: '05', student2: '07', type: 'horizontal' },
        { student1: '05', student2: '07', type: 'all' }
    ];
    // horizontal: same row colDiff 2 → not adjacent → 已遵守
    // all: colDiff 2 → not adjacent → 已遵守
    const report = classifyConstraintReport({ students, constraints, rows: 6 });
    assert(report.pairs[0].status === '已遵守', 'horizontal ok');
    assert(report.pairs[1].status === '已遵守', 'all ok at distance 2');
    assert(report.frontIssues.includes('04'), 'SEN not in front two rows');

    students[1].col = 1; // now adjacent horizontally
    const report2 = classifyConstraintReport({ students, constraints, rows: 6 });
    assert(report2.pairs[0].status === '失敗', 'horizontal fail when adjacent');
    passed++;
}

// 7) 阻擋格
{
    const students = [{ id: '1' }, { id: '2' }];
    const blocked = new Set(['0-0']);
    const result = solveCSP({
        students, rows: 2, cols: 2, blocked, constraints: [],
        opts: { checkerboard: false, disperseGroup: false }
    });
    assert(result.ok, 'with block');
    result.assignment.forEach(([, seat]) => {
        assert(!(seat[0] === 0 && seat[1] === 0), 'not on blocked');
    });
    passed++;
}

// 8) 進階梅花座仍可用（非主軸）
assert(maxCheckerboardCapacity([[0, 0], [0, 1], [1, 0], [1, 1]]) === 2, '2x2 capacity');
passed++;

// 9) 無性別推測
assert(typeof globalThis.guessGender === 'undefined', 'no gender guess');
passed++;

// 10) 學校正式座位表 HTML：標題、教師桌、姓名在非 print-only
{
    const seats = Array.from({ length: 6 }, () => Array(6).fill(null));
    seats[0][0] = { name: '陳志明', id: '01', classGroup: '1B', needsFront: false };
    seats[0][1] = { name: '李美玲', id: '02', classGroup: '1B', needsFront: false };
    const html = buildSchoolFormHtml({
        className: '1B',
        room: '102',
        rows: 6,
        cols: 6,
        seats,
        blockedSeats: new Set(['5-5']),
        teachers: ['王詠珊', '鄭百喬', ''],
        interactive: false
    });
    assert(html.includes('1B班/科座位表 (102室)'), 'official title');
    assert(html.includes('班/科座位表'), 'title phrase');
    assert(html.includes('教師桌'), 'teacher desk');
    assert(html.includes('Class Teacher 1：王詠珊'), 'class teacher 1');
    assert(html.includes('Class Teacher 2：鄭百喬'), 'class teacher 2');
    assert(html.includes('陳志明'), 'student name visible');
    assert(html.includes('李美玲'), 'second name visible');
    assert(!html.includes('print-only'), 'not print-only wrapper');
    assert(!html.includes('終極課室座位表'), 'no product brand on form');
    assert(html.includes('school-aisle'), 'center aisle for even cols');
    assert(html.includes('擋'), 'blocked seat mark');
    const titleIdx = html.indexOf('1B班/科座位表');
    const nameIdx = html.indexOf('陳志明');
    const deskIdx = html.indexOf('教師桌');
    assert(titleIdx < nameIdx && nameIdx < deskIdx, 'title then names then teacher desk');
    const emptyTitle = formatSchoolFormTitle('', '');
    assert(emptyTitle === '　班/科座位表 (　室)', 'blank class/room placeholders');
    assert(schoolFormGridColumns(6).includes('18px'), '6-col aisle track');
    assert(!schoolFormGridColumns(5).includes('18px'), 'odd cols no aisle');
    passed++;
}

console.log(`OK: ${passed} test groups passed`);
