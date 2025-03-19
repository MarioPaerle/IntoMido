from midiutil import MIDIFile

class BasicComposer:
    def __init__(self, tempo=120, channel=0, volume=100, program=0):
        """
        Initialize the Composer Object:
        :param tempo: int, BPM of the midi
        :param channel: int, channel of the midi
        :param volume: int, volume of the midi
        """
        self.midi = MIDIFile(1)  # Un file MIDI con una sola traccia
        self.midi.addTempo(0, 0, tempo)
        self.channel = channel
        self.volume = volume
        self.current_time = 0.0  # Tempo corrente (in beats)
        self.midi.addProgramChange(0, channel, 0, program)

    def _parse_timestep(self, timestep):
        """
        Parses the timestep string for example "1/4" or "6/8"
        """
        try:
            num, denom = map(int, timestep.split('/'))
        except Exception as e:
            raise ValueError("Wrong format'") from e

        return 4 * (num / denom)

    def add_notes_fixed_timestep(self, notes, timestep='1/4', mode='tie', repeataslong=False):
        """
        Aggiunge una sequenza di note al file MIDI.

        Parametri:
          - notes: lista di note. Gli elementi possono essere:
                   * un valore numerico (o convertibile a int) per indicare il pitch della nota;
                   * il carattere '-' per indicare che la nota precedente va "legata" (tie) e la sua durata deve estendersi.
          - timestep: durata base di ogni elemento espresso come frazione (es. '1/8' per un’ottava nota).
          - mode: modalità di interpretazione dei trattini.
                  * 'tie' (default): ogni trattino dopo una nota estende la durata della nota precedente.
                  * 'rest': il trattino viene interpretato come una pausa (rest), incrementando il tempo senza suonare.
        """
        base_duration = self._parse_timestep(timestep)
        i = 0

        if repeataslong:
            notes2 = []
            for i, note in enumerate(notes):
                if i > 0 and note == notes[i-1]:
                    notes2.append('-')
                else:
                    notes2.append(note)

            notes = notes2
        ct = self.current_time
        while i < len(notes):
            elem = notes[i]
            if elem == '-':
                ct += base_duration
                i += 1
            else:
                try:
                    pitch = int(elem)
                except Exception as e:
                    raise ValueError(f"Valore nota non valido: {elem}") from e

                total_duration = base_duration
                if mode == 'tie':
                    # Controlla se le note successive sono trattini e, in tal caso, estendi la durata
                    while (i + 1 < len(notes)) and (notes[i + 1] == '-'):
                        total_duration += base_duration
                        i += 1
                # Aggiungi la nota con la durata totale calcolata
                self.midi.addNote(track=0, channel=self.channel, pitch=pitch,
                                  time=ct, duration=total_duration,
                                  volume=self.volume)
                ct += total_duration
                i += 1

    def tomidi(self, filename):
        """
        Salva il file MIDI nel percorso specificato.
        """
        with open(filename, "wb") as f:
            self.midi.writeFile(f)