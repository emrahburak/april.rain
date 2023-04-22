import sys, random,os,re, queue, time, shutil, socket, json, asyncio, threading
import dataset
import threading
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from collections import deque
from flask import Flask, request, jsonify
import event_emitter as events


class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:  # This is the only difference
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance


class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


class TestQueue(Singleton):
    def __init__(self):
        self.queue = queue.Queue()
        self._lock = threading.Lock()
        self._em = events.EventEmitter()
        self._em.on('hello',self.process_of_queue)
       
    def to_queue(self, file):
        self.queue.put(file)

    def trigger(self):
        self.process_of_queue()

    def get_items(self):
        my_list = list(self.queue.queue)
        return my_list

    def emit(self):
        self._em.emit('hello',name="ebg")

    def process_of_queue(self,name):
        self._lock.acquire()

        if not self.queue.empty():
            item = self.queue.get()

        self._lock.release()

        with dataset.connect(f'sqlite:///test.db') as db:
            db_entry = str(item)
            title =  db_entry + "-" + str(random.random() * 100)
            db['updates'].insert(
                dict(title=title.capitalize(), text=db_entry))

    pass



test_queue = TestQueue()

def socket_listener():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('http://localhost', 5000))
    server_socket.listen()

    print('Socket dinleme başlatıldı.')

    while True:
        # Socket bağlantılarını kabul et
        client_socket, address = server_socket.accept()
        print(f"{address} ile bağlantı kuruldu.")

        # Gelen veriyi al
        data = client_socket.recv(1024).decode('utf-8')
        # Alınan veriyi JSON formatına dönüştür
        json_data = json.loads(data)

        # JSON verisini kullan
        print(f"Gelen veri: {json_data}")



class FileQueue:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.queue_for_args = queue.Queue()
        self.deque_for_text_toFile = deque()
        self.queue_for_title_toFile = queue.Queue()
        self.deque_for_text_toDb = deque()
        self.queue_for_title_toDb = queue.Queue()
        self.destination_folder = 'destination'
        self.db_name = 'recognized.db'

    def populate_queue(self):
        args_files = sys.argv[1:]
        for file in args_files:
            if file.endswith('mp3') and os.path.isfile(file):
                file_path = os.path.abspath(file)
                self.queue_for_args.put(
                    file_path
                )
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

    def to_file(self):
        if not os.path.isdir(self.destination_folder):
            os.mkdir(self.destination_folder)

        while not self.queue_for_title_toFile.empty():
            title = self.queue_for_title_toFile.get()

            with open(title, "w+", encoding='utf-8') as file:
                text = self.deque_for_text_toFile.popleft()

                for text_line in text.split('.'):
                    file.write(text_line+'\n')

                file.close()
                shutil.move(os.path.abspath(title) if os.path.isfile(
                    title) else None, self.destination_folder)

        print("Done: to_file")
        return self

    def to_db(self):

        with dataset.connect(f'sqlite:///{self.db_name}') as db:
            while not self.queue_for_title_toDb.empty():
                title = self.queue_for_title_toDb.get()

                db_entry = self.deque_for_text_toDb.popleft()

                db['updates'].insert(
                    dict(title=title.capitalize(), text=db_entry))

            print("Done: to_db")

        return self

    def cleanUp_workspace(self):
        pattern = re.compile(r'^[0-9]{2}-audio_chunks$')

        for directory in os.listdir('.'):
            full_path = os.path.join('.', directory)
            if os.path.isdir(directory) and pattern.match(directory):
                print(f'Deleting directory: {full_path}')
                shutil.rmtree(full_path)

        print("Done: cleanUp_workspace")
        return self

    def fake_populate_queue(self, file_name):
        self.queue_for_args.put(file_name)
        print('Queue length: ', str(self.queue_for_args.qsize()))
        return self

    def fake_process_queue(self):
        while not self.queue_for_args.empty():
            fake_sound_file = self.queue_for_args.get()
            print(fake_sound_file)
            self.queue_for_title_toFile.put(file_name)
            self.queue_for_title_toDb.put(file_name.replace('.txt', ''))

        return self

    def fake_to_file(self):
        while not self.queue_for_title_toFile.empty():
            fake_file_name = self.queue_for_title_toFile.get()
            print("creating text file for: ", fake_file_name)

        return self

    def fake_cleanup(self):
        print("cleanup work space")
        return self

    def fake_to_db(self):
        while not self.queue_for_title_toDb.empty():
            fake_db_entry = self.queue_for_title_toDb.get()
            print("fake to db for: ", fake_db_entry)
        return self


def process_files(file_list):

    print("Alınan dosya listese: ", file_list)




if __name__ == '__main__':
    socket_listener()
   # file_queue = FileQueue()
   # file_queue.populate_queue().process_queue().to_file().cleanUp_workspace().to_db()
   # file_queue.cleanUp_workspace()
