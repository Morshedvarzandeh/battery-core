# battery-core — open-source battery engineering fundamentals.
# Copyright (C) 2026 Morshed Varzandeh and battery-core contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Synthesise the background bed for a module clip.

Writes a 16-bit stereo WAV of a given length. Everything is generated here, so a
clip carries no third-party audio and nothing to clear for rights.

The bed is deliberately plain: a I-V-vi-IV progression in C major, plucked
arpeggios with a short decay over a quiet pad and a root note per bar. Plucks
and a major key are what keep it from reading as a drone; sustained minor
chords with slow swells sound like a thriller, which is not the brief.

    python3 music.py out.wav 59.3
"""

import math
import struct
import sys
import wave

SR = 48_000
BPM = 100.0
BEAT = 60.0 / BPM          # 0.60 s
BAR = 4 * BEAT             # 2.40 s
STEP = BAR / 8             # 0.30 s, eight plucks to the bar

# I - V - vi - IV in C major, one bar each. Voicings are low so the plucks can
# sit an octave above them without crowding the narration space.
PROGRESSION = [
    [130.81, 164.81, 196.00, 261.63, 329.63],   # C  major
    [98.00, 123.47, 146.83, 196.00, 246.94],    # G  major
    [110.00, 130.81, 164.81, 220.00, 261.63],   # A  minor
    [87.31, 110.00, 130.81, 174.61, 220.00],    # F  major
]
ARP = [0, 2, 3, 4, 3, 2, 3, 4]                  # index into the voicing

PLUCK_GAIN = 0.26
PAD_GAIN = 0.13
BASS_GAIN = 0.22
FADE_IN = 2.0
FADE_OUT = 4.0
TARGET_PEAK = 0.72


def pluck(phase: float, age: float) -> float:
    """A struck string: two quiet harmonics over the fundamental, fast decay."""
    env = math.exp(-age * 6.5)
    return env * (
        math.sin(phase)
        + 0.30 * math.sin(2 * phase)
        + 0.12 * math.sin(3 * phase)
    )


def render(duration: float) -> list[float]:
    n = int(duration * SR)
    out = [0.0] * n
    bars = int(duration / BAR) + 2

    for b in range(bars):
        chord = PROGRESSION[b % len(PROGRESSION)]
        bar_t0 = b * BAR

        # one root note per bar, an octave below the voicing
        f = chord[0] * 0.5
        start = int(bar_t0 * SR)
        for i in range(start, min(n, start + int(1.8 * SR))):
            age = (i - start) / SR
            env = math.exp(-age * 1.9)
            out[i] += BASS_GAIN * env * math.sin(2 * math.pi * f * age)

        # the pad: three chord tones, breathing in and out across the bar
        for f in chord[:3]:
            for i in range(start, min(n, start + int(BAR * SR) + int(0.3 * SR))):
                age = (i - start) / SR
                env = min(1.0, age / 0.35) * math.exp(-age * 0.85)
                out[i] += PAD_GAIN / 3 * env * math.sin(2 * math.pi * f * age)

        # eight plucks, an octave up, alternating across the stereo field later
        for s, idx in enumerate(ARP):
            f = chord[idx] * 2.0
            s0 = int((bar_t0 + s * STEP) * SR)
            if s0 >= n:
                break
            # accent the downbeat, keep the off-beats light
            gain = PLUCK_GAIN * (1.0 if s % 4 == 0 else 0.62)
            w = 2 * math.pi * f
            for i in range(s0, min(n, s0 + int(0.9 * SR))):
                age = (i - s0) / SR
                out[i] += gain * pluck(w * age, age)
    return out


def reverb(buf: list[float]) -> list[float]:
    """Two short taps — enough space to sound like a room, not a cathedral."""
    for delay, gain in ((0.087, 0.26), (0.131, 0.17)):
        d = int(delay * SR)
        for i in range(d, len(buf)):
            buf[i] += gain * buf[i - d]
    return buf


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "music.wav"
    duration = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0

    buf = reverb(render(duration))

    peak = max(abs(v) for v in buf) or 1.0
    scale = TARGET_PEAK / peak
    n = len(buf)
    frames = bytearray()
    for i, v in enumerate(buf):
        t = i / SR
        env = min(1.0, t / FADE_IN)
        if t > duration - FADE_OUT:
            env *= max(0.0, (duration - t) / FADE_OUT)
        s = v * scale * env
        # a touch of width: the right channel is delayed by ~11 ms
        j = i - int(0.011 * SR)
        r = (buf[j] * scale * env) if j >= 0 else 0.0
        left = int(max(-1.0, min(1.0, s)) * 32767)
        right = int(max(-1.0, min(1.0, 0.55 * s + 0.45 * r)) * 32767)
        frames += struct.pack("<hh", left, right)

    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(bytes(frames))
    print(f"{path}: {n / SR:.2f} s, peak {peak * scale:.2f}")


if __name__ == "__main__":
    main()
