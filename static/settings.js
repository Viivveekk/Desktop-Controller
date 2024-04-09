const SettingsElements = {
    emitTimer: {
        input: document.getElementById('emit-timer-input'),
        text: document.getElementById('emit-timer-value'),
        defaultValue: 5
    },
    clickTimeThreshold: {
        input: document.getElementById('click-time-threshold-input'),
        text: document.getElementById('click-time-threshold-value'),
        defaultValue: 180
    },
    clickDistThreshold: {
        input: document.getElementById('click-dist-threshold-input'),
        text: document.getElementById('click-dist-threshold-value'),
        defaultValue: 20
    },
    scrollSpeed: {
        input: document.getElementById('scroll-speed-input'),
        text: document.getElementById('scroll-speed-value'),
        defaultValue: 1.0
    },
    mouseSpeed: {
        input: document.getElementById('mouse-speed-input'),
        text: document.getElementById('mouse-speed-value'),
        defaultValue: 1.0
    },
    darkMode: {
        input: document.getElementById('toggle-darkmode-button'),
        defaultValue: true
    },
    leftHanded: {
        input: document.getElementById('toggle-left-handed-button'),
        defaultValue: false
    },
    scrollThreshold: {
        input: document.getElementById('scroll-threshold-input'),
        text: document.getElementById('scroll-threshold-value'),
        defaultValue: 5
    }
};

let settings = {};

// Fetch a setting from localStorage or fall back to default
function getSetting(key) {
    return localStorage.getItem(key) || SettingsElements[key]['defaultValue'];
}

// Store a setting in localStorage
function setSetting(key, value) {
    localStorage.setItem(key, value);
}

// Update a setting's UI elements
function updateSettingUI(key, value) {
    if (key === 'darkMode') {
        toggleDarkMode(value);        
    } else if (key === 'leftHanded') {
        toggleLeftHanded(value);
    } else {
        value = Number(value);
        SettingsElements[key]['input'].value = value;
        if (Number.isInteger(value)) {
            SettingsElements[key]['text'].textContent = value;
        } else {
            SettingsElements[key]['text'].textContent = value.toFixed(1);
        }
    }
    if (key === 'scrollThreshold' || key === 'leftHanded' || key === 'darkMode') {
        updateGradient();
    }
}

// Load all settings from localStorage into the settings object and update the UI
function loadSettings() {
    for (const key of Object.keys(SettingsElements)) {
        settings[key] = getSetting(key);
        updateSettingUI(key, settings[key]);
    }
    settings.realizedScrollSpeed = Math.pow(10, settings.scrollSpeed - 1);
    settings.realizedMouseSpeed = Math.pow(10, settings.mouseSpeed - 1);
    return settings;
}

// Reset all settings to their default values
function resetSettings() {
    localStorage.clear();
    loadSettings();
}


// Function to toggle dark mode
function toggleDarkMode(value) {
    if (value) {
        document.getElementById('root').classList.add('dark-mode');
    }
    else {
        document.getElementById('root').classList.remove('dark-mode');
    }
}

function toggleLeftHanded(value) {
    if (value) {
        document.getElementById('toggle-left-handed-button').classList.add('fa-flip-horizontal');
    }
    else {
        document.getElementById('toggle-left-handed-button').classList.remove('fa-flip-horizontal');
    }
}

function updateGradient() {
    let value = settings['scrollThreshold'];
    let direction = settings['leftHanded'] ? 'to left' : 'to right';
    let mousePadColor = settings['darkMode'] ? 'rgba(33,33,33,1)' : 'rgba(255,255,255,1)';
    let scrollPadColor = settings['darkMode'] ? 'rgba(68,68,68,1)' : 'rgba(204,204,204,1)';
    let gradient = `linear-gradient(${direction}, ${mousePadColor} ${100-value}%, ${scrollPadColor} ${100-value}%, ${scrollPadColor} 100%)`;
    document.getElementById('trackpad').style.background = gradient;
}

// Attach event listeners for the settings UI
function attachSettingListeners(settings) {
    for (const key of Object.keys(SettingsElements)) {
        let inputType = 'input';
        if (key === 'darkMode' || key === 'leftHanded') {
            inputType = 'click';
        }
        SettingsElements[key]['input'].addEventListener(inputType, (event) => {
            let value = parseFloat(event.target.value);
            if (key === 'darkMode' || key === 'leftHanded') {
                value = !settings[key];
            }
            setSetting(key, value);
            settings[key] = value;
            updateSettingUI(key, value);
            if (key === 'scrollSpeed') {
                settings.realizedScrollSpeed = Math.pow(10, value - 1);
            } else if (key === 'mouseSpeed') {
                settings.realizedMouseSpeed = Math.pow(10, value - 1);
            }
        });
    }
}

// Export a function that initializes everything
export function initSettings() {
    const settings = loadSettings();
    attachSettingListeners(settings);
    document.getElementById('reset-settings-button').addEventListener('click', resetSettings);
    document.getElementById('settings-button').addEventListener('click', () => {
        document.getElementById('settings-panel').classList.toggle('show');
        document.getElementById('settings-button').classList.toggle('rotate');
    });
    return settings;
}