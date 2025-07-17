import os
import re
from pydub import AudioSegment
from pydub.utils import which
import speech_recognition as sr
from pydub.utils import make_chunks
from transformers import pipeline
from pytube import YouTube

# Ensure ffmpeg is installed and accessible
ffmpeg_path = which("ffmpeg")
if not ffmpeg_path:
    raise Exception("ffmpeg not found. Please install ffmpeg and add it to your system's PATH.")

# Load the summarization model (Use T5 for better handling of long texts)
summarizer = pipeline("summarization", model="t5-small")

def extract_video_id(youtube_iframe_link):
    """Extract the YouTube video ID from an iframe link."""
    try:
        # Use regex to extract the video ID
        match = re.search(r'/embed/([a-zA-Z0-9_-]+)', youtube_iframe_link)
        if match:
            return match.group(1)
        else:
            raise Exception("Invalid YouTube iframe link: Video ID not found.")
    except Exception as e:
        raise Exception(f"Error extracting video ID: {e}")

def download_youtube_video(video_id, output_path="temp_video.mp4", max_duration=900):
    """
    Download the first 10-15 minutes of a YouTube video.
    max_duration is in seconds (e.g., 900 seconds = 15 minutes).
    """
    try:
        # Create a YouTube object
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")

        # Get the best quality stream
        stream = yt.streams.filter(progressive=True, file_extension="mp4").first()

        # Download the video
        stream.download(output_path=".", filename=output_path)

        # Trim the video to the first 10-15 minutes
        video = AudioSegment.from_file(output_path)
        trimmed_video = video[:max_duration * 1000]  # Trim to max_duration (in milliseconds)
        trimmed_video.export(output_path, format="mp4")

        return output_path
    except Exception as e:
        raise Exception(f"Error downloading YouTube video: {e}")

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

def generate_summary_from_youtube(youtube_iframe_link):
    """
    Generate a summary from a YouTube iframe link.
    Input: YouTube iframe link.
    Output: Summary text with overview, body, and conclusion.
    """
    try:
        # Step 1: Extract video ID from the iframe link
        video_id = extract_video_id(youtube_iframe_link)

        # Step 2: Download the first 10-15 minutes of the video
        video_file = "temp_video.mp4"
        download_youtube_video(video_id, video_file)

        # Step 3: Convert video to audio
        audio_file = "temp_audio.mp3"
        convert_video_to_audio(video_file, audio_file)

        # Step 4: Convert audio to WAV format
        wav_file = convert_to_wav(audio_file)

        # Step 5: Split audio into chunks
        chunk_files = split_audio(wav_file)

        # Step 6: Convert each chunk to text
        all_text = []
        for chunk_file in chunk_files:
            text = convert_audio_to_text(chunk_file)
            if text:
                all_text.append(text)
            os.remove(chunk_file)  # Clean up chunk file

        # Combine text from all chunks
        final_text = "\n".join(all_text)

        # Step 7: Summarize the text
        summary = summarize_large_text(final_text[:10000])  # Limit to 10000 characters

        # Format the summary
        summary_lines = summary.split("\n")
        overview = "\n".join(summary_lines[:2])
        conclusion = "\n".join(summary_lines[-2:])
        body = "\n".join(summary_lines[2:-2])

        formatted_summary = f"Overview:\n{overview}\n\nBody:\n{body}\n\nConclusion:\n{conclusion}"

        # Clean up temporary files
        os.remove(video_file)
        os.remove(audio_file)
        os.remove(wav_file)

        return formatted_summary

    except Exception as e:
        # Clean up temporary files in case of error
        if os.path.exists("temp_video.mp4"):
            os.remove("temp_video.mp4")
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")
        if os.path.exists(wav_file):
            os.remove(wav_file)
        raise Exception(f"Error generating summary: {e}")
iframe_link = '<iframe width="560" height="315" src="https://www.youtube.com/embed/dX8396ZmSPk?si=i8r48WAlAJ7QZGta" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
summary = generate_summary_from_youtube(iframe_link)
print(summary)