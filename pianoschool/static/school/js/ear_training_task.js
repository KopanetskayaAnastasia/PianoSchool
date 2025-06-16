// --- Карта клавиш ---
const keyNoteMap = new Map([
    ['q','C'],['2','Cs'],['w','D'],['3','Ds'],['e','E'],
    ['r','F'],['5','Fs'],['t','G'],['6','Gs'],['y','A'],['7','As'],['u','B'],
    ['z','C1'],['s','Cs1'],['x','D1'],['d','Ds1'],['c','E1'],
    ['v','F1'],['g','Fs1'],['b','G1'],['h','Gs1'],['n','A1'],['j','As1'],['m','B1'],
    ['i','C2'],['9','Cs2'],['o','D2'],['0','Ds2'],['p','E2'],
    ['[','F2'],['=','Fs2'],[',','G2'],['l','Gs2'],['.','A2'],[';','As2'],['/','B2']
]);

const pressedKeys = new Set();
const pressedMouseKeys = new Set();

// --- Для записи нот ---
let isRecording = false;
let recordedNotes = [];
let recordStartTime = null;

// --- Воспроизведение и подсветка клавиш ---
function playSound(keyElem, highlight=true) {
    let soundId = keyElem.dataset.sound;
    let sound = document.getElementById(soundId);
    if (sound) {
        sound.currentTime = 0;
        sound.play();
    }
    if (highlight) keyElem.classList.add('active');
    if (isRecording) {
        recordedNotes.push({
            note: soundId,
            time: Date.now() - recordStartTime
        });
    }
}

function stopSound(keyElem, unhighlight=true) {
    let soundId = keyElem.dataset.sound;
    let sound = document.getElementById(soundId);
    if (sound) {
        sound.pause();
        sound.currentTime = 0;
    }
    if (unhighlight) keyElem.classList.remove('active');
}

// --- Проигрывание эталонной последовательности с подсветкой ---
function playSequence(sequence, delay=500) {
    let i = 0;
    function playNext() {
        if (i < sequence.length) {
            let keyElem = document.querySelector('.key.' + sequence[i]);
            if (keyElem) playSound(keyElem, true);
            setTimeout(() => {
                if (keyElem) stopSound(keyElem, true);
                i++;
                playNext();
            }, delay);
        }
    }
    playNext();
}

// --- Логика записи ---
function startRecording() {
    isRecording = true;
    recordedNotes = [];
    recordStartTime = Date.now();
}

function stopRecording() {
    isRecording = false;
    return recordedNotes.map(x => x.note);
}

// --- Для csrf ---
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// --- Назначение обработчиков после загрузки DOM ---
document.addEventListener('DOMContentLoaded', function() {
    // Включаем loop для всех аудио
    document.querySelectorAll('audio').forEach(audio => {
        audio.loop = true;
    });

    // --- Клавиатура ---
    document.addEventListener('keydown', function(e){
        if (e.repeat) return;
        const note = keyNoteMap.get(e.key);
        if (note && !pressedKeys.has(e.key)) {
            pressedKeys.add(e.key);
            const keyElem = document.querySelector(".key." + note);
            if (keyElem) playSound(keyElem, true);
        }
    });

    document.addEventListener('keyup', function(e){
        const note = keyNoteMap.get(e.key);
        if (note && pressedKeys.has(e.key)) {
            pressedKeys.delete(e.key);
            const keyElem = document.querySelector(".key." + note);
            if (keyElem) stopSound(keyElem, true);
        }
    });

    // --- Мышь и touch ---
    document.querySelectorAll('.key').forEach(key => {
        key.addEventListener('mousedown', function(e) {
            if (!pressedMouseKeys.has(key)) {
                pressedMouseKeys.add(key);
                playSound(key, true);
            }
        });
        key.addEventListener('mouseup', function(e) {
            if (pressedMouseKeys.has(key)) {
                pressedMouseKeys.delete(key);
                stopSound(key, true);
            }
        });
        key.addEventListener('mouseleave', function(e) {
            if (pressedMouseKeys.has(key)) {
                pressedMouseKeys.delete(key);
                stopSound(key, true);
            }
        });
        // Touch events
        key.addEventListener('touchstart', function(e) {
            e.preventDefault();
            if (!pressedMouseKeys.has(key)) {
                pressedMouseKeys.add(key);
                playSound(key, true);
            }
        }, {passive: false});
        key.addEventListener('touchend', function(e) {
            e.preventDefault();
            if (pressedMouseKeys.has(key)) {
                pressedMouseKeys.delete(key);
                stopSound(key, true);
            }
        }, {passive: false});
        key.addEventListener('touchcancel', function(e) {
            e.preventDefault();
            if (pressedMouseKeys.has(key)) {
                pressedMouseKeys.delete(key);
                stopSound(key, true);
            }
        }, {passive: false});
    });

    // --- Recognition (угадай) ---
    if (window.taskType === 'recognition') {
        const playBtn = document.getElementById('play-sequence-btn');
        if (playBtn) {
            playBtn.onclick = function() {
                playSequence(window.sequence, 500);
            };
        }
        const form = document.getElementById('recognition-form');
        if (form) {
            form.onsubmit = function(e) {
                e.preventDefault();
                const answer = document.querySelector('input[name="answer"]:checked');
                if (!answer) return;
                fetch(window.submitAttemptUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        task_id: window.taskId,
                        selected_option: answer.value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    const result = document.getElementById('result');
                    if (result) {
                        result.innerText = data.is_correct ? "Верно!" : "Неверно!";
                        result.className = data.is_correct ? "" : "wrong";
                    }
                    setTimeout(() => { window.location.reload(); }, 1200);
                });
            };
        }
    }

    // --- Performance (сыграй) ---
    if (window.taskType === 'performance') {
        let playedNotes = [];
        const startBtn = document.getElementById('start-record-btn');
        const stopBtn = document.getElementById('stop-record-btn');
        if (startBtn && stopBtn) {
            startBtn.onclick = function() {
                startRecording();
                startBtn.style.display = 'none';
                stopBtn.style.display = 'inline';
            };
            stopBtn.onclick = function() {
                playedNotes = stopRecording();
                stopBtn.style.display = 'none';
                fetch(window.submitAttemptUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        task_id: window.taskId,
                        played_notes: playedNotes
                    })
                })
                .then(response => response.json())
                .then(data => {
                    const result = document.getElementById('result');
                    if (result) {
                        result.innerText = data.is_correct ? "Верно!" : "Неверно!";
                        result.className = data.is_correct ? "" : "wrong";
                    }
                    setTimeout(() => { window.location.reload(); }, 1200);
                });
            };
        }
    }
});

