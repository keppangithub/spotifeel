import pytest
import promptGPT


class TestIsEmotionValid:
    """Tests for is_emotion_valid function"""
    
    def test_valid_emotion_lowercase(self):
        """Test that valid lowercase emotions return True"""
        assert promptGPT.is_emotion_valid("happy")
        assert promptGPT.is_emotion_valid("furious")
        assert promptGPT.is_emotion_valid("anxious")
        
    def test_valid_emotion_uppercase(self):
        """Test that valid uppercase emotions return True"""
        assert promptGPT.is_emotion_valid("HAPPY")
        assert promptGPT.is_emotion_valid("FURIOUS")
        
    def test_valid_emotion_mixed_case(self):
        """Test that valid mixed case emotions return True"""
        assert promptGPT.is_emotion_valid("Happy")
        assert promptGPT.is_emotion_valid("Furious")
        
    def test_invalid_emotion(self):
        """Test that invalid emotions return False"""
        assert not promptGPT.is_emotion_valid("excited")
        assert not promptGPT.is_emotion_valid("bored")
        assert not promptGPT.is_emotion_valid("")
        
    def test_all_valid_emotions(self):
        """Test all valid emotions from the list"""
        valid_emotions = [
            'furious', 'frustrated', 'horrified', 'disappointed', 
            'euphoric', 'loving', 'happy', 'useless', 'regretful', 
            'dejected', 'unhappy', 'scared', 'anxious'
        ]
        for emotion in valid_emotions:
            assert promptGPT.is_emotion_valid(emotion)


class TestFormatPlaylist:
    """Tests for format_playlist function"""
    
    def test_format_single_song(self):
        """Test formatting a single song"""
        song_list = [["Song Title, Artist Name"]]
        result = promptGPT.format_playlist(song_list)
        
        assert 'tracks' in result
        assert len(result['tracks']) == 1
        assert result['tracks'][0]['titel'] == 'Song Title'
        assert result['tracks'][0]['artists'] == 'Artist Name'
        
    def test_format_multiple_songs(self):
        """Test formatting multiple songs"""
        song_list = [
            ["Song One, Artist One"],
            ["Song Two, Artist Two"],
            ["Song Three, Artist Three"]
        ]
        result = promptGPT.format_playlist(song_list)
        
        assert 'tracks' in result
        assert len(result['tracks']) == 3
        assert result['tracks'][0]['titel'] == 'Song One'
        assert result['tracks'][1]['artists'] == 'Artist Two'
        
    def test_format_empty_list(self):
        """Test formatting an empty list"""
        song_list = []
        result = promptGPT.format_playlist(song_list)
        
        assert 'tracks' in result
        assert len(result['tracks']) == 0
        
    def test_format_invalid_entries_skipped(self):
        """Test that invalid entries (not single element lists) are skipped"""
        song_list = [
            ["Song One, Artist One"],
            ["Invalid", "Multiple", "Elements"],  # Should be skipped
            ["Song Two, Artist Two"]
        ]
        result = promptGPT.format_playlist(song_list)
        
        assert 'tracks' in result
        assert len(result['tracks']) == 2
        
    def test_format_with_extra_whitespace(self):
        """Test formatting with extra whitespace in song data"""
        song_list = [["  Song Title  ,  Artist Name  "]]
        result = promptGPT.format_playlist(song_list)
        
        assert result['tracks'][0]['titel'] == 'Song Title'
        assert result['tracks'][0]['artists'] == 'Artist Name'
