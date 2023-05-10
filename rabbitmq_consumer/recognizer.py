import os,shutil
import time
import logging
import speech_recognition as sr
from queue import Queue as PyQueue
from threading import Thread, Lock
from pydub import AudioSegment
from pydub.silence import split_on_silence
from collections import deque


logging.basicConfig(level=logging.INFO)

CHUNK = os.environ["CHUNK"]


class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


class TestQueue(SingletonClass):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.file = ""
        self.counter = 1
        self._lock = Lock()

    def to_queue(self, file):
        if file.endswith('mp3') and os.path.isfile(file):
            self.file = os.path.abspath(file)


    def cleanup_chunk(self):
        os.system(command)("cd ${CHUNK} && rm -r *")

    def process_of_queue(self):
        # self._lock.acquire()

        song = AudioSegment.from_mp3(self.file)
        chunks = split_on_silence(song,
                                  min_silence_len=500,
                                  silence_thresh=song.dBFS-14,
                                  keep_silence=500
                                  )


        whole_text = ''

        for i, audio_chunk in enumerate(chunks, start=1):
            chunk_filename = os.path.join(
                CHUNK, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")

            with sr.AudioFile(chunk_filename) as source:
                audio_listened = self.recognizer.record(source)

                try:
                    text = self.recognizer.recognize_google(
                        audio_listened, language="tr-TR")

                except sr.UnknownValueError as e:
                    print(
                        f"Error: An error occurred during the speech recognition process for the  {CHUNK}/chunk{i}.wav file and a comprehensible text string could not be provided.")
                except sr.RequestError as e:
                    print(
                        "Could not request results from google Speech Recognition service; {0}".format(e))
                except IOError as e:
                    print("IOError; {0}".format(e))
                else:
                    text = f"{text.capitalize()}. "
                    # print(chunk_filename, ":", sefl.text)
                    whole_text += text
                    time.sleep(0.5)

                finally:
                    os.remove(chunk_filename)
        


        return whole_text

        # self._lock.release()


class FileQueue(SingletonClass):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.queue_for_args = PyQueue()
        self.queue = PyQueue()
        self.destination_folder = 'destination'

    def populate_queue(self, file):
        if file.endswith('mp3') and os.path.isfile(file):
            file_path = os.path.abspath(file)
            self.queue.put(file)

        # args_files = sys.argv[1:]
        # for file in args_files:
        #     if file.endswith('mp3') and os.path.isfile(file):
        #         file_path = os.path.abspath(file)
        #         self.queue_for_args.put(
        #             file_path
        #         )
        print('Done: populate_queue')

        return self

    def process_queue(self):
        counter = 1

        while not self.queue_for_args.empty():
            sound_file = self.queue_for_args.get()
            song = AudioSegment.from_mp3(sound_file)
            chunks = split_on_silence(song,
                                      min_silence_len=500,
                                      silence_thresh=song.dBFS-14,
                                      keep_silence=500
                                      )

            folder_name = f'{str(counter).zfill(2)}-audio_chunks'
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
                counter += 1

            whole_text = ''

            for i, audio_chunk in enumerate(chunks, start=1):
                chunk_filename = os.path.join(
                    folder_name, f"chunk{i}.wav")
                audio_chunk.export(chunk_filename, format="wav")

                with sr.AudioFile(chunk_filename) as source:
                    audio_listened = self.recognizer.record(source)

                    try:
                        text = self.recognizer.recognize_google(
                            audio_listened, language="tr-TR")

                    except sr.UnknownValueError as e:
                        print(
                            f"Error: An error occurred during the speech recognition process for the  {folder_name}/chunk{i}.wav file and a comprehensible text string could not be provided.")
                    except sr.RequestError as e:
                        print(
                            "Could not request results from google Speech Recognition service; {0}".format(e))
                    except IOError as e:
                        print("IOError; {0}".format(e))
                    else:
                        text = f"{text.capitalize()}. "
                        # print(chunk_filename, ":", sefl.text)
                        whole_text += text

                    time.sleep(0.5)

            try:
                self.deque_for_text_toDb.append(whole_text)
                self.deque_for_text_toFile.append(whole_text)

                file_name = f'{os.path.splitext(os.path.basename(sound_file))[0]}.txt'.replace(
                    ' ', '_')
                self.queue_for_title_toFile.put(file_name)
                self.queue_for_title_toDb.put(file_name.replace('.txt', ''))

            except Exception as e:
                print(f"Error: {e}")

        print("Done: process_queue")
        return self
