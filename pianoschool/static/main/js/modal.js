const keyNoteMap = new Map([
    ['q','C'],['2','Cs'],['w','D'],['3','Ds'],['e','E'],
    ['r','F'],['5','Fs'],['t','G'],['6','Gs'],['y','A'],['7','As'],['u','B'],
    ['z','C1'],['s','Cs1'],['x','D1'],['d','Ds1'],['c','E1'],
    ['v','F1'],['g','Fs1'],['b','G1'],['h','Gs1'],['n','A1'],['j','As1'],['m','B1'],
    ['i','C2'],['9','Cs2'],['o','D2'],['0','Ds2'],['p','E2'],
    ['[','F2'],['=','Fs2'],[',','G2'],['l','Gs2'],['.','A2'],[';','As2'],['/','B2']
]);

// Для отслеживания удерживаемых клавиш
const pressedKeys = new Set();

// Для отслеживания удерживаемых мышью/тачем клавиш
const pressedMouseKeys = new Set();

// Для каждого аудио-элемента включаем loop
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
        if (keyElem) {
            keyElem.classList.add('active');
            playSound(keyElem);
        }
    }
});

document.addEventListener('keyup', function(e){
    const note = keyNoteMap.get(e.key);
    if (note && pressedKeys.has(e.key)) {
        pressedKeys.delete(e.key);
        const keyElem = document.querySelector(".key." + note);
        if (keyElem) {
            keyElem.classList.remove('active');
            stopSound(keyElem);
        }
    }
});

// --- Мышь ---
let ke = document.querySelectorAll('.key');
ke.forEach(key => {
    key.addEventListener('mousedown', function(e) {
        if (!pressedMouseKeys.has(key)) {
            pressedMouseKeys.add(key);
            key.classList.add('active');
            playSound(key);
        }
    });

    key.addEventListener('mouseup', function(e) {
        if (pressedMouseKeys.has(key)) {
            pressedMouseKeys.delete(key);
            key.classList.remove('active');
            stopSound(key);
        }
    });

    key.addEventListener('mouseleave', function(e) {
        if (pressedMouseKeys.has(key)) {
            pressedMouseKeys.delete(key);
            key.classList.remove('active');
            stopSound(key);
        }
    });

    // --- Touch ---
    key.addEventListener('touchstart', function(e) {
        e.preventDefault();
        if (!pressedMouseKeys.has(key)) {
            pressedMouseKeys.add(key);
            key.classList.add('active');
            playSound(key);
        }
    }, {passive: false});

    key.addEventListener('touchend', function(e) {
        e.preventDefault();
        if (pressedMouseKeys.has(key)) {
            pressedMouseKeys.delete(key);
            key.classList.remove('active');
            stopSound(key);
        }
    }, {passive: false});

    key.addEventListener('touchcancel', function(e) {
        e.preventDefault();
        if (pressedMouseKeys.has(key)) {
            pressedMouseKeys.delete(key);
            key.classList.remove('active');
            stopSound(key);
        }
    }, {passive: false});
});

// --- Функции воспроизведения и остановки ---
function playSound(keyElem) {
    let soundId = keyElem.dataset.sound;
    let sound = document.getElementById(soundId);
    if (sound) {
        sound.currentTime = 0;
        sound.play();
    }
}

function stopSound(keyElem) {
    let soundId = keyElem.dataset.sound;
    let sound = document.getElementById(soundId);
    if (sound) {
        sound.pause();
        sound.currentTime = 0;
    }
}