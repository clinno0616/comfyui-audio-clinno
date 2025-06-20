import torch
import torchaudio
import numpy as np

class GetAudioDuration:
    """
    計算音頻時長的 ComfyUI 節點，輸出精確到小數點兩位
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
            },
        }
    
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("duration (seconds)",)
    FUNCTION = "get_duration"
    CATEGORY = "audio/analysis"
    
    def get_duration(self, audio):
        """
        計算音頻時長
        
        Args:
            audio: ComfyUI 音頻格式，通常是字典包含 'waveform' 和 'sample_rate'
            
        Returns:
            float: 音頻時長（秒），精確到小數點兩位
        """
        try:
            # 處理不同的音頻輸入格式
            if isinstance(audio, dict):
                # 標準 ComfyUI 音頻格式
                if 'waveform' in audio and 'sample_rate' in audio:
                    waveform = audio['waveform']
                    sample_rate = audio['sample_rate']
                elif 'audio' in audio and 'sample_rate' in audio:
                    waveform = audio['audio']
                    sample_rate = audio['sample_rate']
                else:
                    raise ValueError("不支援的音頻格式")
            elif isinstance(audio, tuple) and len(audio) == 2:
                # (waveform, sample_rate) 格式
                waveform, sample_rate = audio
            else:
                raise ValueError("無法識別的音頻格式")
            
            # 轉換為 torch tensor
            if isinstance(waveform, np.ndarray):
                waveform = torch.from_numpy(waveform)
            
            # 確保 waveform 是 2D tensor (channels, samples)
            if waveform.dim() == 1:
                waveform = waveform.unsqueeze(0)
            elif waveform.dim() == 3:
                # 有些格式可能是 (batch, channels, samples)
                waveform = waveform.squeeze(0)
            
            # 計算時長：樣本數 / 採樣率
            num_samples = waveform.shape[-1]  # 最後一個維度是樣本數
            duration = float(num_samples) / float(sample_rate)
            
            # 四捨五入到小數點兩位
            duration_rounded = round(duration, 2)
            
            return (duration_rounded,)
            
        except Exception as e:
            print(f"計算音頻時長時發生錯誤: {str(e)}")
            return (0.0,)

# 節點映射
NODE_CLASS_MAPPINGS = {
    "GetAudioDuration": GetAudioDuration
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GetAudioDuration": "Get Audio Duration"
}