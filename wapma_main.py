import os, signal, sys, threading, time
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import tkinter as tk
import tkinter.ttk as ttk
from wapma_driver import automation_main

win = tk.Tk()
win.title("WAPMA")

# Main frame configuration
main_frame = ttk.Frame(win, width=600, height=600, padding="10 10 10 10")
main_frame.grid(column=0, row=0, sticky="nsew")
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

# Four compartment frame configurations
# 1st frame
frame_for_retrieving_user_language_setting = tk.Frame(main_frame)
frame_for_retrieving_user_language_setting.grid(column=0,
                                                row=0,
                                                columnspan=2,
                                                rowspan=3,
                                                sticky="nsew",
                                                padx=7,
                                                pady=7)

# 2nd frame
frame_for_retrieving_group_name = tk.Frame(main_frame)
frame_for_retrieving_group_name.grid(column=2,
                                     row=0,
                                     columnspan=2,
                                     rowspan=3,
                                     sticky="nsew",
                                     padx=7,
                                     pady=7)

# 3rd frame
frame_for_retrieving_message_to_send = tk.Frame(main_frame)
frame_for_retrieving_message_to_send.grid(column=0,
                                          row=3,
                                          columnspan=4,
                                          rowspan=3,
                                          pady=7)

# 4th frame
frame_for_running_automation = tk.Frame(main_frame)
frame_for_running_automation.grid(column=0, row=6, columnspan=4, pady=7)

# 5th frame
frame_for_console_log = tk.Frame(main_frame)
frame_for_console_log.grid(column=4, row=0, columnspan=3, rowspan=7, pady=7)


# Class for console logging
class PrintLogger():
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.insert(tk.END, text)

    def flush(self):
        pass


# Functions for user entry retrieval
user_language = tk.StringVar(win, name="user_language")
group_name = tk.StringVar(win, name="group_name")
message_to_send = tk.StringVar(win, name="message_to_send")


def retrieve_user_language():
    win.setvar(name="user_language", value=user_language_combobox.get())
    print("Your WA's language: " + user_language.get())


def retrieve_group_name():
    win.setvar(name="group_name", value=group_name_entry.get())
    print("Your designated group name: " + group_name.get())


def retrieve_message():
    win.setvar(name="message_to_send",
               value=message_textbox.get("1.0", "end-1c"))
    print("The message you're going to send: \n" + message_to_send.get() +
          '\n')


# Functions for running and stopping automation
#list_of_tuples = []
#
#def automation():
#    automation_main(user_language = user_language.get(), group_name = group_name.get(), message_to_send = message_to_send.get())
#
#def run_main():
#    am = threading.Thread(target = automation)
#    am.start()
#    pid = str(os.getpid())
#    thread_id = str(threading.current_thread())
#    gid = str(threading.get_id())
#    list_of_tuples.append((pid,thread_id,gid))
#
#def stop_main():
#    os.kill(int(list_of_tuples[0][0]), signal.SIGTERM)
#
#def debug_main():
#    print("PID, thread ID's and ID's of thread of ran threads: \n" + str(list_of_tuples))
#    print("Current active thread count: " + str(threading.active_count()))
#    print("Current active thread, thread identifier and native id:\n" + str(threading.current_thread()) + "\n" + str(threading.get_ident()) + "\n" + str(threading.get_native_id()))
#    print("All active thread: \n" + str(threading.enumerate()))

#class ThreadFactory:
#    def __init__(self, main_function_name):
#        self.main_function_name = main_function_name
#        self.main_thread_object = None
#        self.term_event = threading.Event()
#        self.count = 0
#
#    def main_thread(self):
#        automation_main(user_language = user_language.get(), group_name = group_name.get(), message_to_send = message_to_send.get())
#
#    def starter(self, thr):
#        try:
#            thr.start()
#            print('Running thread id: ' + str(thr.ident))
#        except Exception:
#            print("Exception thrown in starter method.")
#            return
#
#    def stopper(self):
#        self.term_event.set()
#
#    def controller(self):
#        try:
#            self.main_thread_object = threading.Thread(target = self.main_thread, name = self.main_function_name)
#            self.starter(self.main_thread_object)
#            while not self.term_event.is_set():
#                if self.term_event.is_set():
#                    break
#                self.count = self.count + 1
#        except Exception:
#            print("Exception thrown in controller method.")
#            return
#
#def run_main(thread_factory_class, controller_thread):
#    thread_factory_class.starter(controller_thread)
#
#    print('All currently running threads, before stopper(): ' + str(threading.enumerate()) + '\n')
#
#def stop_main(thread_factory_class, controller_thread):
#    thread_factory_class.stopper()
#
#    if not controller_thread.is_alive():
#    	print('Controller threaded function stopped.')
#    # Fungsi utama belum bisa mati.
#    if not thread_factory_class.main_thread_object.is_alive():
#    	print("Main threaded function stopped.")
#
#    print('All currently running threads, after stopper(): ' + str(threading.enumerate()) + '\n')
#    print("Counter: " + str(thread_factory_class.count))
#
#def debug_main():
#    print("Current active thread count: " + str(threading.active_count()))
#    print("Current active thread, thread identifier and native id:\n" + str(threading.current_thread()) + "\n" + str(threading.get_ident()) + "\n" + str(threading.get_native_id()))
#    print("All active thread: \n" + str(threading.enumerate()))
#
## Thread initialization
#M = ThreadFactory("Main-Thread")
#ct = threading.Thread(target = M.controller, name = "Controller-Thread")

P = mp.Process(target=automation_main,
               kwargs={
                   'user_language': user_language.get(),
                   'group_name': group_name.get(),
                   'message_to_send': message_to_send.get(),
               })


def run_main():
    try:
        P.start()
        print('PID: ' + str(P.pid))
    except SystemExit:
        P.terminate()
        P.join()
        if P.is_alive() is False:
            print('Process terminated, missing parameter/s.')


def stop_main():
    pid = str(P.pid)
    P.terminate()
    P.join()
    if P.is_alive():
        print('Process ' + pid + ' is still alive.')
    else:
        print('Process ' + pid + ' is terminated.')


def debug_main():
    print("Current active process count: " + str(mp.active_children()))
    print("Current active process:\n" + str(mp.current_process()))


# Widgets inside the first frame
user_language_label = ttk.Label(frame_for_retrieving_user_language_setting,
                                text="Your interface's language?")
user_language_label.pack(pady=5, expand=True)

lang_list = ["English", "Indonesian", "Portuguese"]
user_language_combobox = ttk.Combobox(
    frame_for_retrieving_user_language_setting, values=lang_list)
user_language_combobox.set("---")
user_language_combobox.pack(pady=5, expand=True)

user_language_button = ttk.Button(frame_for_retrieving_user_language_setting,
                                  text="Input",
                                  command=retrieve_user_language)
user_language_button.pack(pady=5, expand=True)

# Widgets inside the second frame
group_name_label = ttk.Label(frame_for_retrieving_group_name,
                             text="What's the designated group name?")
group_name_label.pack(pady=5, expand=True)

group_name_entry = tk.Entry(frame_for_retrieving_group_name,
                            highlightcolor="#dfdfdf",
                            width=20)
group_name_entry.pack(pady=5, expand=True)

group_name_button = ttk.Button(frame_for_retrieving_group_name,
                               text="Input",
                               command=retrieve_group_name)
group_name_button.pack(pady=5, expand=True)

# Widgets inside the third frame
message_label = ttk.Label(frame_for_retrieving_message_to_send,
                          text="Type your message:")
message_label.pack(pady=5, expand=True)

message_textbox = tk.Text(frame_for_retrieving_message_to_send,
                          undo=True,
                          height=15,
                          width=50)
message_textbox.pack(pady=5, expand=True)

message_button = ttk.Button(frame_for_retrieving_message_to_send,
                            text="Input",
                            command=retrieve_message)
message_button.pack(pady=5, expand=True)

# Widgets inside the fourth frame
run_stop_automation_label = ttk.Label(
    frame_for_running_automation, text="Click to run or stop the automation")
run_stop_automation_label.grid(column=0,
                               row=0,
                               columnspan=3,
                               sticky="nsew",
                               pady=7)

run_automation_button = tk.Button(frame_for_running_automation,
                                  text="Run",
                                  bg="Green",
                                  command=run_main)
run_automation_button.grid(column=0, row=1)

stop_automation_button = tk.Button(frame_for_running_automation,
                                   text="Stop",
                                   bg="Red",
                                   command=stop_main)
stop_automation_button.grid(column=1, row=1)

debug_automation_button = tk.Button(frame_for_running_automation,
                                    text="Debug",
                                    bg="Gray",
                                    command=debug_main)
debug_automation_button.grid(column=2, row=1)

# Widgets inside the fifth frame
console_log_label = ttk.Label(frame_for_console_log, text="Console log")
console_log_label.pack(pady=5, expand=True)

console_log_textbox = tk.Text(frame_for_console_log, height=28, width=40)
console_log_textbox.pack(pady=5, expand=True)

instantiate_console_log_textbox = PrintLogger(console_log_textbox)
sys.stdout = instantiate_console_log_textbox

win.mainloop()
