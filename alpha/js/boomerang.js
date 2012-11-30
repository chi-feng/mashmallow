var context = new webkitAudioContext();

var buffer; 
var bufferLoaded = false;

var masterGainNode;

function loadBuffer(url) {
    console.log('Loading Buffer');
    var request = new XMLHttpRequest();
    request.open("GET", url, true);
    request.responseType = "arraybuffer";
    request.onload = function() {
    	buffer = context.createBuffer(request.response, false);
        bufferLoaded = true;
        console.log('Buffer Loaded');
    }
    request.send();
}

function init() {
	
	loadBuffer('assets/example/TRRBHAK139155E1516.mp3');

	var finalMixNode;
	if (context.createDynamicsCompressor) {
		compressor = context.createDynamicsCompressor();
		compressor.connect(context.destination);
		finalMixNode = compressor;
	}

	masterGainNode = context.createGainNode();
	masterGainNode.gain.value = 0.4; // reduce overall volume to avoid clipping
	masterGainNode.connect(finalMixNode);

	document.getElementById("reset").addEventListener("mousedown", handleReset, false);
}
/*
function advanceNote() {
	// Advance time by a 16th note... BPM hard coded to 90
	var secondsPerBeat = 60.0 / 90;

	rhythmIndex++;
	if (rhythmIndex == loopLength) {
		rhythmIndex = 1;
	}

	noteTime += secondsPerBeat/4;
}
*/

function playNote(buffer, when, offset, duration) {
	var note = context.createBufferSource();
	note.buffer = buffer;
	note.playbackRate.value = 1.0;
    note.connect(masterGainNode);
	note.start(when, offset, duration);
}

/*
function schedule() {
	var currentTime = context.currentTime;

	currentTime -= startTime;

	while (noteTime < currentTime+ 0.200) {
		var contextPlayTime = noteTime + startTime;
		var playedNotes = [];
		var playMe = true;

		for(i = 0; i < notes.length; i++) {
			if (rhythmIndex == notes[i].beat) {
				for(j = 0; j < playedNotes.length; j++) {
					if (playedNotes[j].sound == notes[i].sound && playedNotes[j].freq == notes[i].freq) {
						playMe = false;
						continue;
					}
				}
				if(playMe) {
					playNote(currentPatch.soundBuffer[(notes[i].freq) + (notes[i].sound)], false, 0,0,-2, 1, 1 * 1.0, 0, contextPlayTime);
					playedNotes.push(notes[i]);
				}
				playMe = true;
			}
		}
		movePlayhead();
		advanceNote();
	}
	timeoutId = setTimeout(schedule, 0);
}

function movePlayhead() {
	playPos.position.z += 62.5;
	if(playPos.position.z  > -467.5 + (62.5*15)) {
		playPos.position.z = -467.5;
	}
	playPos.updateMatrix();
};


function startStop() {
	if(isPlaying) {
		isPlaying = false;
		handleStop();
	} else {
		isPlaying = true;
		handlePlay();
	}
}

function handlePlay(event) {
	noteTime = 0.0;
	startTime = context.currentTime + 0.005;
	schedule();
}

function handleStop(event) {
	clearTimeout(timeoutId);
}
*/

init();

}