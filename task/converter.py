from ffmpeg import FFmpeg

def convert2mp3(from_path, to_path, bitrate='320k'):
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(from_path)
        .output(
            to_path,
            {"codec:a": "libmp3lame", "b:a": bitrate},
        )
    )

    ffmpeg.execute()
