import pytest
import emotionControllerAPI


class TestNegatedFeelingId:
    """Tests for negated_feeling_id function"""
    
    def test_happy_emotion_returns_sad(self):
        """Test that happy emotions return sad emotion"""
        # Test euphoric (5)
        result = emotionControllerAPI.negated_feeling_id(5)
        assert 'unhappy' in result.lower() or 'dejected' in result.lower()
        
    def test_angry_emotion_returns_happy(self):
        """Test that angry emotions return happy emotion"""
        # Test furious (1)
        result = emotionControllerAPI.negated_feeling_id(1)
        assert 'loving' in result.lower() or 'happy' in result.lower()
        
    def test_sad_emotion_returns_happy(self):
        """Test that sad emotions return happy emotion"""
        # Test disappointed (4)
        result = emotionControllerAPI.negated_feeling_id(4)
        assert 'happy' in result.lower() or 'euphoric' in result.lower()


class TestNegatedFeelingStr:
    """Tests for negated_feeling_str function"""
    
    def test_happy_string_returns_opposite(self):
        """Test that happy emotion strings return opposite"""
        result = emotionControllerAPI.negated_feeling_str("happy")
        assert 'unhappy' in result.lower() or 'dejected' in result.lower()
        
    def test_angry_string_returns_opposite(self):
        """Test that angry emotion strings return opposite"""
        result = emotionControllerAPI.negated_feeling_str("furious")
        assert 'loving' in result.lower() or 'happy' in result.lower()
        
    def test_sad_string_returns_opposite(self):
        """Test that sad emotion strings return opposite"""
        result = emotionControllerAPI.negated_feeling_str("disappointed")
        assert 'happy' in result.lower() or 'euphoric' in result.lower()
        
    def test_unknown_emotion_returns_unknown(self):
        """Test that unknown emotion returns 'unknown'"""
        result = emotionControllerAPI.negated_feeling_str("invalid_emotion")
        assert result == "unknown"


class TestGetEmotions:
    """Tests for get_emotions function"""
    
    def test_returns_emotions_list(self):
        """Test that get_emotions returns a non-empty result"""
        result = emotionControllerAPI.get_emotions()
        assert result is not None
