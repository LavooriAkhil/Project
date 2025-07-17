import os
from pydub import AudioSegment
from pydub.utils import which
import speech_recognition as sr
from pydub.utils import make_chunks
from transformers import pipeline

# Ensure ffmpeg is installed and accessible
ffmpeg_path = which("ffmpeg")
if not ffmpeg_path:
    raise Exception("ffmpeg not found. Please install ffmpeg and add it to your system's PATH.")

# Load the summarization model (Use T5 for better handling of long texts)
summarizer = pipeline("summarization", model="t5-small")

def convert_video_to_audio(video_file, output_audio_file):
    """Convert video to audio and save as MP3."""
    try:
        video = AudioSegment.from_file(video_file)
        video.export(output_audio_file, format="mp3")
        return output_audio_file
    except Exception as e:
        raise Exception(f"Error converting video to audio: {e}")

def convert_audio_to_text(audio_file):
    """Convert audio to text using Google Speech Recognition."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        raise Exception("Could not understand audio.")
    except sr.RequestError as e:
        raise Exception(f"Error with Google Speech Recognition service: {e}")
    except Exception as e:
        raise Exception(f"Error processing audio: {e}")

def convert_to_wav(input_file):
    """Convert audio file to WAV format."""
    try:
        output_file = os.path.splitext(input_file)[0] + "_converted.wav"
        audio = AudioSegment.from_file(input_file)
        audio = audio.set_channels(1).set_frame_rate(16000)  # Mono & 16 kHz
        audio.export(output_file, format="wav")
        return output_file
    except Exception as e:
        raise Exception(f"Error converting to WAV: {e}")

def split_audio(input_file, chunk_length_ms=60000):
    """Split audio into 60-second chunks."""
    try:
        audio = AudioSegment.from_file(input_file)
        chunks = make_chunks(audio, chunk_length_ms)
        chunk_files = []
        for i, chunk in enumerate(chunks):
            chunk_file = f"chunk_{i}.wav"
            chunk.export(chunk_file, format="wav")
            chunk_files.append(chunk_file)
        return chunk_files
    except Exception as e:
        raise Exception(f"Error splitting audio: {e}")

def summarize_large_text(text):
    """Summarizes large text in chunks and combines results."""
    chunks = split_text_into_chunks(text)
    summarized_chunks = []

    for chunk in chunks:
        try:
            formatted_text = "summarize: " + chunk
            summary = summarizer(formatted_text, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
            summarized_chunks.append(summary)
        except Exception as e:
            summarized_chunks.append("⚠️ Unable to summarize this part.")

    return "\n\n".join(summarized_chunks)

def split_text_into_chunks(text, chunk_size=300):
    """Split text into smaller chunks for summarization."""
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def generate_summary_from_video(video_file_path):
    """
    Generate a summary from a video file.
    Input: Relative path to the video file.
    Output: Summary text with overview, body, and conclusion.
    """
    try:
        # Step 1: Convert video to audio
        audio_file = "temp_audio.mp3"
        convert_video_to_audio(video_file_path, audio_file)

        # Step 2: Convert audio to WAV format
        wav_file = convert_to_wav(audio_file)

        # Step 3: Split audio into chunks
        chunk_files = split_audio(wav_file)

        # Step 4: Convert each chunk to text
        all_text = []
        for chunk_file in chunk_files:
            text = convert_audio_to_text(chunk_file)
            if text:
                all_text.append(text)
            os.remove(chunk_file)  # Clean up chunk file

        # Combine text from all chunks
        final_text = "\n".join(all_text)

        # Step 5: Summarize the text
        summary = summarize_large_text(final_text[:10000])  # Limit to 10000 characters

        # Format the summary
        summary_lines = summary.split("\n")
        overview = "\n".join(summary_lines[:2])
        conclusion = "\n".join(summary_lines[-2:])
        body = "\n".join(summary_lines[2:-2])

        formatted_summary = f"Overview:\n{overview}\n\nBody:\n{body}\n\nConclusion:\n{conclusion}"

        # Clean up temporary files
        os.remove(audio_file)
        os.remove(wav_file)

        return formatted_summary

    except Exception as e:
        # Clean up temporary files in case of error
        if os.path.exists(audio_file):
            os.remove(audio_file)
        if os.path.exists(wav_file):
            os.remove(wav_file)
        raise Exception(f"Error generating summary: {e}")