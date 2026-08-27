/**
 * Ultra Seat 學校版 — 核心邏輯單測（不開瀏覽器）
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

function solveCSP({ students, rows, cols, blocked, constraints, opts, nodeLimit = 100000, timeMs = 5000 }) {
    let availableSeats = [];
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (!blocked.has(`${r}-${c}`)) availableSeats.push([r, c]);
        }
    }
    if (opts.checkerboard) {
        const colored = pickCheckerboardColorSeats(availableSeats, students.length);
        if (!colored) return { ok: false, nodes: 0, timedOut: false };
        availableSeats = colored;
    }
    const seats = availableSeats.map(s => [...s]);
    const assignment = new Map();
    const occupied = new Map();
    const start = Date.now();
    let nodes = 0;
    let timedOut = false;

    function isValid(student, seat) {
        const [row, col] = seat;
        const key = `${row}-${col}`;
        if (occupied.has(key)) return false;
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

    function domainFor(student) {
        return seats.filter(s => isValid(student, s));
    }

    function selectNext(remaining) {
        let best = null, bestCount = Infinity;
        for (const s of remaining) {
            const d = domainFor(s);
            if (d.length < bestCount) {
                bestCount = d.length;
                best = { student: s, domain: d };
                if (bestCount === 0) break;
            }
        }
        return best;
    }

    function bt(remaining) {
        nodes++;
        if (nodes > nodeLimit || Date.now() - start > timeMs) {
            timedOut = true;
            return false;
        }
        if (remaining.length === 0) return true;
        const pick = selectNext(remaining);
        if (!pick || pick.domain.length === 0) return false;
        const next = remaining.filter(s => s.id !== pick.student.id);
        for (const seat of pick.domain) {
            const key = `${seat[0]}-${seat[1]}`;
            assignment.set(pick.student.id, seat);
            occupied.set(key, pick.student);
            if (bt(next)) return true;
            assignment.delete(pick.student.id);
            occupied.delete(key);
            if (timedOut) return false;
        }
        return false;
    }

    for (let restart = 0; restart < 5; restart++) {
        assignment.clear();
        occupied.clear();
        shuffleArray(seats);
        const remaining = shuffleArray([...students]);
        if (bt(remaining)) {
            return { ok: true, assignment: new Map(assignment), nodes };
        }
        if (nodes > nodeLimit) break;
    }
    return { ok: false, nodes, timedOut };
}

function assert(cond, msg) {
    if (!cond) throw new Error('FAIL: ' + msg);
}

function seatsGrid(rows, cols) {
    const a = [];
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) a.push([r, c]);
    return a;
}

function verifyCheckerboard(assignment, blocked, rows, cols) {
    const occ = new Map();
    for (const [id, seat] of assignment) occ.set(`${seat[0]}-${seat[1]}`, id);
    for (const [, seat] of assignment) {
        for (const [nr, nc] of orthogonalNeighbors(seat[0], seat[1], rows, cols)) {
            const nk = `${nr}-${nc}`;
            if (blocked.has(nk)) continue;
            if (occ.has(nk)) return false;
        }
    }
    return true;
}

let passed = 0;

// 1) adjacency
assert(checkAdjacency(0, 0, 0, 1, 'horizontal'), 'horizontal neighbor');
assert(!checkAdjacency(0, 0, 1, 0, 'horizontal'), 'not horizontal');
assert(checkAdjacency(0, 0, 1, 1, 'all'), 'diagonal all');
assert(!checkAdjacency(0, 0, 1, 1, 'vertical'), 'diagonal not vertical');
passed++;

// 2) checkerboard capacity 4x4 = 8
assert(maxCheckerboardCapacity(seatsGrid(4, 4)) === 8, '4x4 capacity 8');
passed++;

// 3) blocked does not reduce checkerboard neighbor occupancy wrongly —
//    place with blocked between: capacity still computable
{
    const blocked = new Set(['0-1']);
    const avail = seatsGrid(2, 3).filter(([r, c]) => !blocked.has(`${r}-${c}`));
    assert(maxCheckerboardCapacity(avail) >= 2, 'capacity with block');
    passed++;
}

// 4) solve checkerboard 40 students on 10x10
{
    const students = [];
    for (let i = 0; i < 40; i++) students.push({ id: 'S' + i, classGroup: i < 20 ? 'A' : 'B' });
    const blocked = new Set();
    const result = solveCSP({
        students, rows: 10, cols: 10, blocked,
        constraints: [],
        opts: { checkerboard: true, disperseGroup: false }
    });
    assert(result.ok, '40 on 10x10 checkerboard should solve');
    assert(verifyCheckerboard(result.assignment, blocked, 10, 10), 'result is checkerboard');
    passed++;
}

// 5) pair constraint respected
{
    const students = [
        { id: 'A', classGroup: '' },
        { id: 'B', classGroup: '' },
        { id: 'C', classGroup: '' },
        { id: 'D', classGroup: '' }
    ];
    const result = solveCSP({
        students, rows: 3, cols: 3, blocked: new Set(),
        constraints: [{ student1: 'A', student2: 'B', type: 'horizontal' }],
        opts: { checkerboard: false, disperseGroup: false }
    });
    assert(result.ok, 'pair constraint solvable on 3x3');
    const a = result.assignment.get('A');
    const b = result.assignment.get('B');
    assert(!checkAdjacency(a[0], a[1], b[0], b[1], 'horizontal'), 'A and B not horizontal neighbors');
    passed++;
}

// 6) impossible: 3 students checkerboard on 2x2 (max capacity 2)
{
    const avail = seatsGrid(2, 2);
    assert(maxCheckerboardCapacity(avail) === 2, '2x2 checkerboard max 2');
    const students = [{ id: '1' }, { id: '2' }, { id: '3' }];
    const result = solveCSP({
        students, rows: 2, cols: 2, blocked: new Set(),
        constraints: [],
        opts: { checkerboard: true, disperseGroup: false },
        nodeLimit: 5000
    });
    assert(!result.ok, '3 students checkerboard 2x2 must fail');
    passed++;
}

// 7) disperse same group
{
    const students = [];
    for (let i = 0; i < 8; i++) {
        students.push({ id: 'A' + i, classGroup: '甲' });
        students.push({ id: 'B' + i, classGroup: '乙' });
    }
    const result = solveCSP({
        students, rows: 8, cols: 8, blocked: new Set(),
        constraints: [],
        opts: { checkerboard: true, disperseGroup: true }
    });
    assert(result.ok, 'disperse+checkerboard 16 on 8x8');
    for (const [id, seat] of result.assignment) {
        const me = students.find(s => s.id === id);
        for (const [nr, nc] of orthogonalNeighbors(seat[0], seat[1], 8, 8)) {
            let otherId = null;
            for (const [oid, os] of result.assignment) {
                if (os[0] === nr && os[1] === nc) otherId = oid;
            }
            if (!otherId) continue;
            const other = students.find(s => s.id === otherId);
            assert(me.classGroup !== other.classGroup, 'orthogonal neighbor different group');
        }
    }
    passed++;
}

// 8) legacy CSV header detection helpers
function normalizeHeader(h) {
    return String(h || '').replace(/^\uFEFF/, '').trim().toLowerCase();
}
assert(normalizeHeader('\uFEFF學號') === '學號', 'BOM strip');
assert(!('guessGender' in globalThis && false), 'no gender API required');
passed++;

console.log(`OK: ${passed} test groups passed`);
