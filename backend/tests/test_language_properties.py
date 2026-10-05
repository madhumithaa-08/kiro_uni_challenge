"""Property tests for language detection (task 6.2, requirement 1.2)."""

from hypothesis import given, strategies as st

from app.domain.language import KNOWN_LANGUAGES, detect_language, extension_for


@given(st.text(), st.one_of(st.none(), st.text()))
def test_detect_is_total_and_in_known_set(code: str, filename) -> None:
    lang = detect_language(code, filename)
    assert lang in KNOWN_LANGUAGES


@given(st.text(), st.one_of(st.none(), st.text()))
def test_detect_is_deterministic(code: str, filename) -> None:
    assert detect_language(code, filename) == detect_language(code, filename)


@given(st.sampled_from(sorted(KNOWN_LANGUAGES)))
def test_extension_nonempty_for_known_languages(lang: str) -> None:
    ext = extension_for(lang)
    assert ext and ext.isalnum()
