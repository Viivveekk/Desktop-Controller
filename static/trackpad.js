import { initSettings } from "./settings.js";

const settings = initSettings();

const socket = io();
const trackpad = document.getElementById('trackpad');
let currentTouch = null;
let lastTouch = null;
let touchStartTime = null;
let touchEndTime = null;
let emitInterval = null;
let scrollInterval = null;
let mouseUpTimeOut = null;
let clickStart = null;
let clicked = false;
let dragging = false;

function scroll(touches) {
    if (touches.length == 2) {
        currentTouch = lastTouch = {
            clientX: (touches[0].clientX + touches[1].clientX) / 2,
            clientY: (touches[0].clientY + touches[1].clientY) / 2
        };
    } else {
        currentTouch = lastTouch = { clientX: touches[0].clientX, clientY: touches[0].clientY };
    }
    scrollInterval = setInterval(() => {
        if (currentTouch && lastTouch) {
            let dy = currentTouch.clientY - lastTouch.clientY;
            socket.emit('scroll', { dy: dy * settings.realizedScrollSpeed });
            lastTouch = { clientX: currentTouch.clientX, clientY: currentTouch.clientY };
        }
    }, settings.emitTimer);
}

function mouseMove(touches) {
    currentTouch = lastTouch = { clientX: touches[0].clientX, clientY: touches[0].clientY };
    let broken = false;
    emitInterval = setInterval(() => {
        if (lastTouch && currentTouch) {
            let dx = currentTouch.clientX - lastTouch.clientX;
            let dy = currentTouch.clientY - lastTouch.clientY;
            let detlaX = currentTouch.clientX - clickStart.clientX;
            let detlaY = currentTouch.clientY - clickStart.clientY;
            if (!broken && (Date.now() - touchStartTime < settings.clickTimeThreshold && Math.hypot(detlaX, detlaY) < settings.clickDistThreshold)) {
                dx = 0
                dy = 0
            } else {
                broken = true;
            }
            socket.emit('mousemove', { dx: dx * settings.realizedMouseSpeed, dy: dy * settings.realizedMouseSpeed });
            lastTouch = { clientX: currentTouch.clientX, clientY: currentTouch.clientY };
        }
    }, settings.emitTimer);
}

trackpad.addEventListener('touchstart', (event) => {
    clickStart = event.touches[0];
    dragging = false;
    event.preventDefault(); // Prevent scrolling while touching
    newTouch();
    touchStartTime = Date.now();
    const touches = event.touches;
    if (touchEndTime) {
        if (Date.now() - touchEndTime > settings.clickTimeThreshold) {
            clicked = false;
        } else {
            clearTimeout(mouseUpTimeOut);
        }
    } else {
        clicked = false;
    }
    if (touches.length === 1) {
        let distanceFromEdge = touches[0].clientX/window.innerWidth;
        if (settings.leftHanded ? (distanceFromEdge < settings.scrollThreshold/100) : (distanceFromEdge > (100-settings.scrollThreshold)/100)) {
            scroll(touches);
        } else if (clicked) {
            mouseMove(touches);
            dragging = true;
        } else {
            mouseMove(touches)
        }
    } else if (touches.length === 2) {
        scroll(touches);
    }
});

trackpad.addEventListener('touchmove', (event) => {
    event.preventDefault(); // Prevent scrolling while touching
    const touch = event.touches[0];
    currentTouch = { clientX: touch.clientX, clientY: touch.clientY };
});

trackpad.addEventListener('touchend', () => {
    if(Date.now() - touchStartTime < settings.clickTimeThreshold) {
        socket.emit('mouseup');
        dragging = false;
    }
    clicked = false;
    if (currentTouch) {
        let deltaY = currentTouch.clientX - clickStart.clientX;
        let deltaX = currentTouch.clientY - clickStart.clientY;
        touchEndTime = Date.now();
        const touchDuration = touchEndTime - touchStartTime;
        
        if (!dragging && touchDuration < settings.clickTimeThreshold && Math.hypot(deltaX, deltaY) < settings.clickDistThreshold) {
            clicked = true;
            socket.emit('mousedown');
        }
    }
    if (dragging || clicked) {
        mouseUpTimeOut = setTimeout(() => {
            socket.emit('mouseup')
            dragging = false;
        }, settings.clickTimeThreshold);
    }
});

// Method to handle chagen in touches
function newTouch() {
    reset();
    currentTouch = lastTouch = null;
    touchStartTime = null;
}

function reset() {
    if (emitInterval) {
        clearInterval(emitInterval);
        emitInterval = null;
    }
    if (scrollInterval) {
        clearInterval(scrollInterval);
        scrollInterval = null;
    }
}