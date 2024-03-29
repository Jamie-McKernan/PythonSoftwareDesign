import pytest

from src.design_principles.solid.single_responsibility.example import (
    BadSoundSpeaker,
    BestSoundSpeaker,
    GoodSoundSpeaker,
)
from src.design_principles.solid.single_responsibility.supplement import (
    FLACFile,
    MP3File,
    SoundData,
    WAVFile,
)


def test_can_instantiate_bad_speaker() -> None:
    # when
    speaker = BadSoundSpeaker()

    # then
    assert isinstance(speaker, BadSoundSpeaker)
    assert not speaker.powered_on


def test_can_power_on_bad_speaker() -> None:
    # given
    speaker = BadSoundSpeaker()

    # when
    speaker.power_on()

    # then
    assert speaker.powered_on


def test_can_instantiate_mp3_music_file() -> None:
    # when
    music_file = MP3File(data=b"great music")

    # then
    assert isinstance(music_file, MP3File)


def test_can_play_mp3_music_from_bad_speaker() -> None:
    # given
    music_data = b"great music"
    music_file = MP3File(data=music_data)

    speaker = BadSoundSpeaker()
    speaker.power_on()

    # when
    speaker_output = speaker.play_music(music_file)

    # then
    assert speaker_output == SoundData(music_data)


@pytest.mark.xfail(reason="This test demonstrates an anti-pattern.", strict=True)
def test_can_play_wav_music_from_bad_speaker() -> None:
    # given
    music_data = b"great music"
    music_file = WAVFile(data=music_data)

    speaker = BadSoundSpeaker()
    speaker.power_on()

    # when
    speaker_output = speaker.play_music(music_file)  # type: ignore[arg-type]

    # then
    assert speaker_output == music_data


def test_can_instantiate_sound_data() -> None:
    # when
    music_data = b"music data"
    sound = SoundData(music_data)

    # then
    assert isinstance(sound, SoundData)


def test_can_instantiate_good_speaker() -> None:
    # when
    speaker = GoodSoundSpeaker()

    # then
    assert isinstance(speaker, GoodSoundSpeaker)
    assert not speaker.powered_on


def test_can_power_on_good_speaker() -> None:
    # given
    speaker = GoodSoundSpeaker()

    # when
    speaker.power_on()

    # then
    assert speaker.powered_on


def test_can_play_mp3_music_from_good_speaker() -> None:
    # given
    music_data = b"great music"
    music_file = MP3File(data=music_data)

    speaker = GoodSoundSpeaker()
    speaker.power_on()

    # when
    raw_sound_data = music_file.stream_mp3_data()
    speaker_output = speaker.play_sound(raw_sound_data)

    # then
    assert speaker_output == SoundData(music_data)


def test_can_play_wav_music_from_good_speaker() -> None:
    # given
    music_data = b"great music"
    music_file = WAVFile(data=music_data)

    speaker = GoodSoundSpeaker()
    speaker.power_on()

    # when
    raw_sound_data = music_file.stream_wav_data()
    speaker_output = speaker.play_sound(raw_sound_data)

    # then
    assert speaker_output == SoundData(music_data)


def test_can_play_flac_music_from_best_speaker() -> None:
    # given
    music_data = b"great music"
    music_file = FLACFile(data=music_data)

    speaker = BestSoundSpeaker()
    speaker.power_on()

    # when
    speaker_output = speaker.play_sound(music_file)

    # then
    assert speaker_output == SoundData(music_data)
